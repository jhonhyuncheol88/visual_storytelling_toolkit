from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from typing import Optional


@dataclass
class Asset:
    id: Optional[int]
    kind: str
    original_path: str | None
    project_path: str
    filename: str
    ext: str
    width: int | None
    height: int | None
    duration_sec: float | None
    hash_sha256: str
    tags: str | None
    thumbnail_path: str | None


class AssetRepository:
    def __init__(self, db_path: str) -> None:
        self._db_path = db_path

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def get_by_hash(self, sha256: str) -> Optional[Asset]:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM Assets WHERE hash_sha256=?", (sha256,)).fetchone()
            if not row:
                return None
            return self._row_to_asset(row)

    def get_by_id(self, asset_id: int) -> Optional[Asset]:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM Assets WHERE id=?", (asset_id,)).fetchone()
            return self._row_to_asset(row) if row else None

    def upsert_image(self, *,
                     original_path: str | None,
                     project_path: str,
                     filename: str,
                     ext: str,
                     width: int | None,
                     height: int | None,
                     hash_sha256: str,
                     thumbnail_path: str | None) -> int:
        existing = self.get_by_hash(hash_sha256)
        if existing:
            return int(existing.id or 0)
        with self._connect() as conn:
            cur = conn.execute(
                """
                INSERT INTO Assets(kind, original_path, project_path, filename, ext, width, height, duration_sec, hash_sha256, tags, thumbnail_path)
                VALUES('image',?,?,?,?,?,?,NULL,?,NULL,?)
                """,
                (original_path, project_path, filename, ext, width, height, hash_sha256, thumbnail_path),
            )
            return int(cur.lastrowid)

    def update_tags(self, asset_id: int, tags: str) -> None:
        with self._connect() as conn:
            conn.execute("UPDATE Assets SET tags=? WHERE id=?", (tags, asset_id))

    def is_asset_referenced(self, asset_id: int) -> bool:
        with self._connect() as conn:
            # Referenced by Characters.image_asset_id or Shots.storyboard_asset_id
            c = conn.execute("SELECT COUNT(*) AS cnt FROM Characters WHERE image_asset_id=?", (asset_id,)).fetchone()[
                0
            ]
            s = conn.execute(
                "SELECT COUNT(*) AS cnt FROM Shots WHERE storyboard_asset_id=?",
                (asset_id,),
            ).fetchone()[0]
            return int(c or 0) + int(s or 0) > 0

    def delete_asset(self, asset_id: int) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM Assets WHERE id=?", (asset_id,))

    def _row_to_asset(self, row: sqlite3.Row) -> Asset:
        return Asset(
            id=row["id"],
            kind=row["kind"],
            original_path=row["original_path"],
            project_path=row["project_path"],
            filename=row["filename"],
            ext=row["ext"],
            width=row["width"],
            height=row["height"],
            duration_sec=row["duration_sec"],
            hash_sha256=row["hash_sha256"],
            tags=row["tags"],
            thumbnail_path=row["thumbnail_path"],
        )


