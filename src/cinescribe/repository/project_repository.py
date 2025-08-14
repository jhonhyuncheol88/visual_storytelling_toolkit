from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from typing import Optional


@dataclass
class ProjectInfo:
    id: int
    title: str
    logline: str
    synopsis: str
    intent: str
    review_notes: str


class ProjectRepository:
    def __init__(self, db_path: str) -> None:
        self._db_path = db_path

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def get_info(self) -> Optional[ProjectInfo]:
        with self._connect() as conn:
            row = conn.execute("SELECT id, title, logline, synopsis, intent, review_notes FROM Project_Info WHERE id=1").fetchone()
            if not row:
                return None
            return ProjectInfo(
                id=int(row["id"]),
                title=row["title"] or "",
                logline=row["logline"] or "",
                synopsis=row["synopsis"] or "",
                intent=row["intent"] or "",
                review_notes=row["review_notes"] or "",
            )

    def update_title(self, title: str) -> None:
        with self._connect() as conn:
            conn.execute(
                "UPDATE Project_Info SET title=?, updated_at=datetime('now') WHERE id=1",
                (title,),
            )

    def update_logline_synopsis(self, logline: str | None = None, synopsis: str | None = None) -> None:
        sets = []
        params = []
        if logline is not None:
            sets.append("logline=?")
            params.append(logline)
        if synopsis is not None:
            sets.append("synopsis=?")
            params.append(synopsis)
        if not sets:
            return
        sets.append("updated_at=datetime('now')")
        sql = f"UPDATE Project_Info SET {' , '.join(sets)} WHERE id=1"
        with self._connect() as conn:
            conn.execute(sql, tuple(params))


