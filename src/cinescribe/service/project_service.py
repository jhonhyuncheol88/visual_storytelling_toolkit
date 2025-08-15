from __future__ import annotations

from typing import Optional

from ..repository.project_repository import ProjectRepository, ProjectInfo


class ProjectService:
    def __init__(self, db_path: str) -> None:
        self._repo = ProjectRepository(db_path)

    def load_info(self) -> Optional[ProjectInfo]:
        return self._repo.get_info()

    def save_title(self, title: str) -> None:
        self._repo.update_title(title)

    def save_logline_synopsis(self, logline: str | None = None, synopsis: str | None = None) -> None:
        self._repo.update_logline_synopsis(logline=logline, synopsis=synopsis)

    def update_tags(self, tags: str) -> None:
        """프로젝트 태그 업데이트"""
        self._repo.update_tags(tags)

    def get_tags(self) -> str:
        """프로젝트 태그 조회"""
        return self._repo.get_tags()

    def add_tag(self, tag: str) -> None:
        """기존 태그에 새 태그 추가 (중복 방지)"""
        self._repo.add_tag(tag)

    def remove_tag(self, tag: str) -> None:
        """특정 태그 제거"""
        self._repo.remove_tag(tag)


