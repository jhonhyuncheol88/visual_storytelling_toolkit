from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class Document:
    id: Optional[int]
    key: str
    format: str  # 'json' | 'text'
    content: str  # raw text; json은 문자열로 보관
    updated_at: Optional[str] = None


class DocumentRepository:
    def __init__(self, db_path: str) -> None:
        self._db_path = db_path
        self._ensure_schema()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _ensure_schema(self) -> None:
        with self._connect() as conn:
            # 여러 구문을 한 번에 실행해야 하므로 executescript 사용
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS Documents (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  key TEXT NOT NULL UNIQUE,
                  format TEXT NOT NULL CHECK (format IN ('json','text')),
                  content TEXT NOT NULL,
                  updated_at TEXT DEFAULT (datetime('now'))
                );
                CREATE INDEX IF NOT EXISTS idx_documents_key ON Documents(key);
                """
            )

    def upsert(self, doc: Document) -> int:
        with self._connect() as conn:
            cur = conn.execute(
                """
                INSERT INTO Documents(key, format, content)
                VALUES(?,?,?)
                ON CONFLICT(key) DO UPDATE SET
                  format=excluded.format,
                  content=excluded.content,
                  updated_at=datetime('now')
                ;
                """,
                (doc.key, doc.format, doc.content),
            )
            return int(cur.lastrowid or 0)

    def get(self, key: str) -> Optional[Document]:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM Documents WHERE key=?", (key,)).fetchone()
            if not row:
                return None
            return Document(
                id=row["id"],
                key=row["key"],
                format=row["format"],
                content=row["content"],
                updated_at=row["updated_at"],
            )

    def export_to_file(self, key: str, out_path: str) -> None:
        doc = self.get(key)
        if not doc:
            raise FileNotFoundError(key)
        mode = "w"
        with open(out_path, mode, encoding="utf-8") as f:
            if doc.format == "json":
                # pretty print
                try:
                    parsed = json.loads(doc.content)
                except json.JSONDecodeError:
                    parsed = doc.content
                if isinstance(parsed, (dict, list)):
                    f.write(json.dumps(parsed, ensure_ascii=False, indent=2))
                else:
                    f.write(str(parsed))
            else:
                f.write(doc.content)


