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
class Shot:
    id: int
    scene_id: int
    code: str
    description: str
    storyboard_asset_id: int | None
    sort_index: int | None
    asset_thumbnail_path: str | None = None
    asset_project_path: str | None = None
    shot_type: str | None = None
    angle: str | None = None
    movement: str | None = None
    lens: str | None = None
    lighting: str | None = None
    image_prompt: str | None = None
    video_prompt: str | None = None


class SceneShotRepository:
    def __init__(self, db_path: str) -> None:
        self._db_path = db_path

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row
        return conn

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

    def update_scene_notes(self, scene_id: int, notes: str) -> None:
        with self._connect() as conn:
            conn.execute("UPDATE Scenes SET summary=? WHERE id=?", (notes, scene_id))

    def list_shots(self, scene_id: int) -> List[Shot]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT s.id,
                       s.scene_id,
                       COALESCE(s.code,'') AS code,
                       COALESCE(s.description,'') AS description,
                       s.storyboard_asset_id,
                       s.sort_index,
                       s.shot_type,
                       s.angle,
                       s.movement,
                       s.lens,
                       s.lighting,
                       s.image_prompt,
                       s.video_prompt,
                       a.thumbnail_path AS asset_thumbnail_path,
                       a.project_path AS asset_project_path
                  FROM Shots s
                  LEFT JOIN Assets a ON a.id = s.storyboard_asset_id
                 WHERE s.scene_id=?
                 ORDER BY s.sort_index ASC, s.id ASC
                """,
                (scene_id,),
            ).fetchall()
            shots: List[Shot] = []
            for r in rows:
                shots.append(
                    Shot(
                        id=r["id"],
                        scene_id=r["scene_id"],
                        code=r["code"],
                        description=r["description"],
                        storyboard_asset_id=r["storyboard_asset_id"],
                        sort_index=r["sort_index"],
                        asset_thumbnail_path=r["asset_thumbnail_path"],
                        asset_project_path=r["asset_project_path"],
                        shot_type=r["shot_type"],
                        angle=r["angle"],
                        movement=r["movement"],
                        lens=r["lens"],
                        lighting=r["lighting"],
                        image_prompt=r["image_prompt"],
                        video_prompt=r["video_prompt"],
                    )
                )
            return shots

    def create_shot(self, scene_id: int, code: str = "", description: str = "", asset_id: int | None = None) -> int:
        with self._connect() as conn:
            cur = conn.execute(
                "INSERT INTO Shots(scene_id, code, description, storyboard_asset_id, sort_index) VALUES(?,?,?,?, (SELECT COALESCE(MAX(sort_index),0)+1 FROM Shots WHERE scene_id=?))",
                (scene_id, code, description, asset_id, scene_id),
            )
            return int(cur.lastrowid)

    def link_shot_asset(self, shot_id: int, asset_id: int | None) -> None:
        with self._connect() as conn:
            conn.execute("UPDATE Shots SET storyboard_asset_id=? WHERE id=?", (asset_id, shot_id))

    def update_shot_meta(self, shot_id: int, code: str | None = None, description: str | None = None) -> None:
        sets = []
        params = []
        if code is not None:
            sets.append("code=?")
            params.append(code)
        if description is not None:
            sets.append("description=?")
            params.append(description)
        if not sets:
            return
        sql = f"UPDATE Shots SET {' , '.join(sets)} WHERE id=?"
        params.append(shot_id)
        with self._connect() as conn:
            conn.execute(sql, tuple(params))

    def update_shots_order(self, scene_id: int, ordered_shot_ids: List[int]) -> None:
        with self._connect() as conn:
            for idx, sid in enumerate(ordered_shot_ids, start=1):
                conn.execute("UPDATE Shots SET sort_index=? WHERE id=? AND scene_id=?", (idx, sid, scene_id))

    def get_shot(self, shot_id: int) -> Optional[Shot]:
        with self._connect() as conn:
            r = conn.execute(
                """
                SELECT s.id, s.scene_id, COALESCE(s.code,'') AS code, COALESCE(s.description,'') AS description,
                       s.storyboard_asset_id, s.sort_index, s.shot_type, s.angle, s.movement, s.lens, s.lighting,
                       s.image_prompt, s.video_prompt
                  FROM Shots s WHERE s.id=?
                """,
                (shot_id,),
            ).fetchone()
            if not r:
                return None
            return Shot(
                id=r["id"],
                scene_id=r["scene_id"],
                code=r["code"],
                description=r["description"],
                storyboard_asset_id=r["storyboard_asset_id"],
                sort_index=r["sort_index"],
                shot_type=r["shot_type"],
                angle=r["angle"],
                movement=r["movement"],
                lens=r["lens"],
                lighting=r["lighting"],
                image_prompt=r["image_prompt"],
                video_prompt=r["video_prompt"],
            )

    def delete_shot(self, shot_id: int) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM Shots WHERE id=?", (shot_id,))

    def duplicate_shot(self, shot_id: int) -> Optional[int]:
        sh = self.get_shot(shot_id)
        if not sh:
            return None
        with self._connect() as conn:
            cur = conn.execute(
                """
                INSERT INTO Shots(scene_id, code, description, storyboard_asset_id, sort_index, shot_type, angle, movement, lens, lighting, image_prompt, video_prompt)
                VALUES(?,?,?,?, (SELECT COALESCE(MAX(sort_index),0)+1 FROM Shots WHERE scene_id=?), ?,?,?,?,?,?,?)
                """,
                (
                    sh.scene_id,
                    sh.code,
                    sh.description,
                    sh.storyboard_asset_id,
                    sh.scene_id,
                    sh.shot_type,
                    sh.angle,
                    sh.movement,
                    sh.lens,
                    sh.lighting,
                    sh.image_prompt,
                    sh.video_prompt,
                ),
            )
            return int(cur.lastrowid)

    def update_shot_details(
        self,
        shot_id: int,
        *,
        shot_type: str | None = None,
        angle: str | None = None,
        movement: str | None = None,
        lens: str | None = None,
        lighting: str | None = None,
        image_prompt: str | None = None,
        video_prompt: str | None = None,
    ) -> None:
        sets = []
        params: list = []
        if shot_type is not None:
            sets.append("shot_type=?")
            params.append(shot_type)
        if angle is not None:
            sets.append("angle=?")
            params.append(angle)
        if movement is not None:
            sets.append("movement=?")
            params.append(movement)
        if lens is not None:
            sets.append("lens=?")
            params.append(lens)
        if lighting is not None:
            sets.append("lighting=?")
            params.append(lighting)
        if image_prompt is not None:
            sets.append("image_prompt=?")
            params.append(image_prompt)
        if video_prompt is not None:
            sets.append("video_prompt=?")
            params.append(video_prompt)
        if not sets:
            return
        sql = f"UPDATE Shots SET {' , '.join(sets)} WHERE id=?"
        params.append(shot_id)
        with self._connect() as conn:
            conn.execute(sql, tuple(params))

    def delete_scene(self, scene_id: int) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM Scenes WHERE id=?", (scene_id,))

    def move_scene(self, scene_id: int, direction: int) -> None:
        # direction: -1 up, +1 down
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT id, sort_index FROM Scenes ORDER BY sort_index ASC, id ASC"
            ).fetchall()
            idx_map = [r["id"] for r in rows]
            if scene_id not in idx_map:
                return
            i = idx_map.index(scene_id)
            j = i + direction
            if j < 0 or j >= len(idx_map):
                return
            a_id = idx_map[i]
            b_id = idx_map[j]
            a_sort = rows[i]["sort_index"] or (i + 1)
            b_sort = rows[j]["sort_index"] or (j + 1)
            conn.execute("UPDATE Scenes SET sort_index=? WHERE id=?", (b_sort, a_id))
            conn.execute("UPDATE Scenes SET sort_index=? WHERE id=?", (a_sort, b_id))


