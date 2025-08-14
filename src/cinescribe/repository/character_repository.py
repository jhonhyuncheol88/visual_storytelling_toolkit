from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Character:
    id: int
    name: str
    age: str | None = None
    job: str | None = None
    personality: str | None = None
    goal: str | None = None
    conflict: str | None = None
    design_prompt: str | None = None
    image_asset_id: int | None = None


class CharacterRepository:
    def __init__(self, db_path: str) -> None:
        self._db_path = db_path

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def list_characters(self) -> List[Character]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT id, name, age, job, personality, goal, conflict, design_prompt, image_asset_id
                  FROM Characters
                 ORDER BY id ASC
                """
            ).fetchall()
            return [self._row_to_model(r) for r in rows]

    def get(self, char_id: int) -> Optional[Character]:
        with self._connect() as conn:
            r = conn.execute(
                "SELECT id, name, age, job, personality, goal, conflict, design_prompt, image_asset_id FROM Characters WHERE id=?",
                (char_id,),
            ).fetchone()
            return self._row_to_model(r) if r else None

    def create(self, name: str) -> int:
        with self._connect() as conn:
            cur = conn.execute("INSERT INTO Characters(name) VALUES(?)", (name,))
            return int(cur.lastrowid)

    def update(self, char_id: int, **fields) -> None:
        if not fields:
            return
        sets = []
        params: list = []
        for k, v in fields.items():
            sets.append(f"{k}=?")
            params.append(v)
        sql = f"UPDATE Characters SET {', '.join(sets)} WHERE id=?"
        params.append(char_id)
        with self._connect() as conn:
            conn.execute(sql, tuple(params))

    def link_image(self, char_id: int, asset_id: int | None) -> None:
        with self._connect() as conn:
            conn.execute("UPDATE Characters SET image_asset_id=? WHERE id=?", (asset_id, char_id))

    def delete(self, char_id: int) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM Characters WHERE id=?", (char_id,))

    def _row_to_model(self, row: sqlite3.Row) -> Character:
        return Character(
            id=row["id"],
            name=row["name"],
            age=row["age"],
            job=row["job"],
            personality=row["personality"],
            goal=row["goal"],
            conflict=row["conflict"],
            design_prompt=row["design_prompt"],
            image_asset_id=row["image_asset_id"],
        )


