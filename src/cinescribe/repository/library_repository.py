from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from typing import Iterable, List, Optional

from ..utils.paths import get_library_db_path


@dataclass
class LibraryProject:
    id: Optional[int]
    title: str
    project_path: str
    tags: str
    thumbnail: Optional[str]
    last_opened_at: Optional[str]
    created_at: Optional[str]
    db_version: Optional[int]
    archived: int = 0


class LibraryRepository:
    def __init__(self) -> None:
        self._db_path = get_library_db_path()
        self._ensure_schema()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _ensure_schema(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS projects (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT NOT NULL,
                  project_path TEXT NOT NULL UNIQUE,
                  tags TEXT DEFAULT '',
                  thumbnail TEXT,
                  last_opened_at TEXT,
                  created_at TEXT DEFAULT (datetime('now')),
                  db_version INTEGER,
                  archived INTEGER DEFAULT 0
                );
                """
            )
            conn.execute("CREATE INDEX IF NOT EXISTS idx_projects_title ON projects(title);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_projects_tags ON projects(tags);")

    def upsert_project(self, p: LibraryProject) -> int:
        with self._connect() as conn:
            cur = conn.execute(
                """
                INSERT INTO projects(title, project_path, tags, thumbnail, last_opened_at, db_version, archived)
                VALUES(?,?,?,?,?,?,?)
                ON CONFLICT(project_path) DO UPDATE SET
                  title=excluded.title,
                  tags=excluded.tags,
                  thumbnail=excluded.thumbnail,
                  last_opened_at=excluded.last_opened_at,
                  db_version=excluded.db_version,
                  archived=excluded.archived
                ;
                """,
                (
                    p.title,
                    p.project_path,
                    p.tags,
                    p.thumbnail,
                    p.last_opened_at,
                    p.db_version,
                    p.archived,
                ),
            )
            return int(cur.lastrowid or 0)

    def list_projects(self, query: str = "", include_archived: bool = False) -> List[LibraryProject]:
        where = []
        params: List[object] = []
        if query:
            where.append("(title LIKE ? OR tags LIKE ?)")
            like = f"%{query}%"
            params.extend([like, like])
        if not include_archived:
            where.append("archived=0")
        where_sql = (" WHERE " + " AND ".join(where)) if where else ""
        # SQLite에는 NULLS LAST 문법이 없으므로 IS NULL을 통해 정렬
        sql = f"SELECT * FROM projects{where_sql} ORDER BY (last_opened_at IS NULL) ASC, last_opened_at DESC, created_at DESC"
        with self._connect() as conn:
            rows = conn.execute(sql, params).fetchall()
            return [self._row_to_model(r) for r in rows]

    def archive(self, project_path: str, archived: bool = True) -> None:
        with self._connect() as conn:
            conn.execute("UPDATE projects SET archived=? WHERE project_path=?", (1 if archived else 0, project_path))

    def remove(self, project_path: str) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM projects WHERE project_path=?", (project_path,))

    def mark_opened_now(self, project_path: str) -> None:
        with self._connect() as conn:
            conn.execute(
                "UPDATE projects SET last_opened_at=datetime('now') WHERE project_path=?",
                (project_path,),
            )

    def _row_to_model(self, row: sqlite3.Row) -> LibraryProject:
        return LibraryProject(
            id=row["id"],
            title=row["title"],
            project_path=row["project_path"],
            tags=row["tags"],
            thumbnail=row["thumbnail"],
            last_opened_at=row["last_opened_at"],
            created_at=row["created_at"],
            db_version=row["db_version"],
            archived=int(row["archived"] or 0),
        )


