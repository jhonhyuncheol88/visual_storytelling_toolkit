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
    tags: str = ""


class ProjectRepository:
    def __init__(self, db_path: str) -> None:
        self._db_path = db_path
        self._ensure_schema()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _ensure_schema(self) -> None:
        """스키마 자동 업그레이드: tags 컬럼이 없으면 추가"""
        with self._connect() as conn:
            try:
                # tags 컬럼이 있는지 확인
                conn.execute("SELECT tags FROM Project_Info LIMIT 1")
            except sqlite3.OperationalError:
                # tags 컬럼이 없으면 추가
                print("Project_Info 테이블에 tags 컬럼 추가 중...")
                conn.execute("ALTER TABLE Project_Info ADD COLUMN tags TEXT DEFAULT ''")
                print("tags 컬럼 추가 완료")

    def get_info(self) -> Optional[ProjectInfo]:
        with self._connect() as conn:
            row = conn.execute("SELECT id, title, logline, synopsis, intent, review_notes, COALESCE(tags, '') as tags FROM Project_Info WHERE id=1").fetchone()
            if not row:
                return None
            return ProjectInfo(
                id=int(row["id"]),
                title=row["title"] or "",
                logline=row["logline"] or "",
                synopsis=row["synopsis"] or "",
                intent=row["intent"] or "",
                review_notes=row["review_notes"] or "",
                tags=row["tags"] or "",
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

    def update_tags(self, tags: str) -> None:
        """프로젝트 태그 업데이트"""
        with self._connect() as conn:
            conn.execute(
                "UPDATE Project_Info SET tags=?, updated_at=datetime('now') WHERE id=1",
                (tags,),
            )

    def get_tags(self) -> str:
        """프로젝트 태그 조회"""
        with self._connect() as conn:
            row = conn.execute("SELECT COALESCE(tags, '') as tags FROM Project_Info WHERE id=1").fetchone()
            return row["tags"] if row else ""

    def add_tag(self, tag: str) -> None:
        """기존 태그에 새 태그 추가 (중복 방지)"""
        current_tags = self.get_tags()
        if current_tags:
            tag_list = [t.strip() for t in current_tags.split(",") if t.strip()]
            if tag not in tag_list:
                tag_list.append(tag)
                new_tags = ", ".join(tag_list)
            else:
                new_tags = current_tags
        else:
            new_tags = tag
        self.update_tags(new_tags)

    def remove_tag(self, tag: str) -> None:
        """특정 태그 제거"""
        current_tags = self.get_tags()
        if current_tags:
            tag_list = [t.strip() for t in current_tags.split(",") if t.strip() and t.strip() != tag]
            new_tags = ", ".join(tag_list)
            self.update_tags(new_tags)


