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


