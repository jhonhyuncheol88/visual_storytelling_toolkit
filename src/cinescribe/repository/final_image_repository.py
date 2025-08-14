from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Scene:
    id: int
    number: int
    name: str
    notes: str | None = None


@dataclass
class FinalImage:
    id: int
    scene_id: int
    description: str
    asset_id: int | None
    sort_index: int | None
    asset_thumbnail_path: str | None = None
    asset_project_path: str | None = None


class FinalImageRepository:
    def __init__(self, db_path: str) -> None:
        self._db_path = db_path
        self._ensure_schema()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _ensure_schema(self) -> None:
        with self._connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS FinalImages (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  scene_id INTEGER NOT NULL,
                  description TEXT DEFAULT '',
                  asset_id INTEGER NULL,
                  sort_index INTEGER,
                  updated_at TEXT DEFAULT (datetime('now')),
                  FOREIGN KEY(scene_id) REFERENCES Scenes(id) ON DELETE CASCADE,
                  FOREIGN KEY(asset_id) REFERENCES Assets(id) ON DELETE SET NULL
                );
                CREATE INDEX IF NOT EXISTS idx_final_images_scene ON FinalImages(scene_id);
                """
            )

    # Scenes는 기존 테이블을 그대로 사용한다.
    def list_scenes(self) -> List[Scene]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT id, COALESCE(number, id) AS number, COALESCE(name,'') AS name, COALESCE(summary,'') AS notes FROM Scenes ORDER BY number ASC, id ASC"
            ).fetchall()
            return [Scene(id=row["id"], number=row["number"], name=row["name"], notes=row["notes"]) for row in rows]

    def create_scene(self, number: int | None = None, name: str | None = None, notes: str | None = None) -> int:
        with self._connect() as conn:
            cur = conn.execute(
                "INSERT INTO Scenes(number, name, summary, sort_index) VALUES(?,?,?, (SELECT COALESCE(MAX(sort_index),0)+1 FROM Scenes))",
                (number, name, notes),
            )
            return int(cur.lastrowid)

    # FinalImages CRUD
    def list_images(self, scene_id: int) -> List[FinalImage]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT f.id,
                       f.scene_id,
                       COALESCE(f.description,'') AS description,
                       f.asset_id,
                       f.sort_index,
                       a.thumbnail_path AS asset_thumbnail_path,
                       a.project_path AS asset_project_path
                  FROM FinalImages f
             LEFT JOIN Assets a ON a.id = f.asset_id
                 WHERE f.scene_id=?
              ORDER BY f.sort_index ASC, f.id ASC
                """,
                (scene_id,),
            ).fetchall()
            images: List[FinalImage] = []
            for r in rows:
                images.append(
                    FinalImage(
                        id=r["id"],
                        scene_id=r["scene_id"],
                        description=r["description"],
                        asset_id=r["asset_id"],
                        sort_index=r["sort_index"],
                        asset_thumbnail_path=r["asset_thumbnail_path"],
                        asset_project_path=r["asset_project_path"],
                    )
                )
            return images

    def create_image(self, scene_id: int, description: str = "", asset_id: int | None = None) -> int:
        with self._connect() as conn:
            cur = conn.execute(
                "INSERT INTO FinalImages(scene_id, description, asset_id, sort_index) VALUES(?,?,?, (SELECT COALESCE(MAX(sort_index),0)+1 FROM FinalImages WHERE scene_id=?))",
                (scene_id, description, asset_id, scene_id),
            )
            return int(cur.lastrowid)

    def link_image_asset(self, image_id: int, asset_id: int | None) -> None:
        with self._connect() as conn:
            conn.execute("UPDATE FinalImages SET asset_id=? WHERE id=?", (asset_id, image_id))

    def update_image_meta(self, image_id: int, description: str | None = None) -> None:
        sets = []
        params: list = []
        if description is not None:
            sets.append("description=?")
            params.append(description)
        if not sets:
            return
        sql = f"UPDATE FinalImages SET {' , '.join(sets)} WHERE id=?"
        params.append(image_id)
        with self._connect() as conn:
            conn.execute(sql, tuple(params))

    def update_images_order(self, scene_id: int, ordered_image_ids: List[int]) -> None:
        with self._connect() as conn:
            for idx, iid in enumerate(ordered_image_ids, start=1):
                conn.execute("UPDATE FinalImages SET sort_index=? WHERE id=? AND scene_id=?", (idx, iid, scene_id))

    def delete_image(self, image_id: int) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM FinalImages WHERE id=?", (image_id,))


