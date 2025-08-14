from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class CinematicBoard:
    id: int
    format: str  # 'json' | 'text'
    content: str
    updated_at: Optional[str] = None


class CinematicRepository:
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
                CREATE TABLE IF NOT EXISTS CinematicBoard (
                  id INTEGER PRIMARY KEY CHECK (id = 1),
                  format TEXT NOT NULL CHECK (format IN ('json','text')),
                  content TEXT NOT NULL,
                  updated_at TEXT DEFAULT (datetime('now'))
                );
                INSERT OR IGNORE INTO CinematicBoard(id, format, content) VALUES(1, 'json', '{}');
                """
            )

    def upsert(self, format: str, content: str) -> int:
        with self._connect() as conn:
            cur = conn.execute(
                """
                INSERT INTO CinematicBoard(id, format, content)
                VALUES(1, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                  format=excluded.format,
                  content=excluded.content,
                  updated_at=datetime('now')
                ;
                """,
                (format, content),
            )
            return int(cur.lastrowid or 1)

    def get(self) -> Optional[CinematicBoard]:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM CinematicBoard WHERE id=1").fetchone()
            if not row:
                return None
            return CinematicBoard(
                id=row["id"],
                format=row["format"],
                content=row["content"],
                updated_at=row["updated_at"],
            )

    def export_to_file(self, out_path: str) -> None:
        board = self.get()
        if not board:
            raise FileNotFoundError("CinematicBoard")
        with open(out_path, "w", encoding="utf-8") as f:
            if board.format == "json":
                try:
                    parsed = json.loads(board.content)
                except json.JSONDecodeError:
                    parsed = board.content
                if isinstance(parsed, (dict, list)):
                    f.write(json.dumps(parsed, ensure_ascii=False, indent=2))
                else:
                    f.write(str(parsed))
            else:
                f.write(board.content)


