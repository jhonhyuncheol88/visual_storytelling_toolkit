from __future__ import annotations

import os
from typing import List

from ..repository.library_repository import LibraryRepository, LibraryProject


class LibraryService:
    def __init__(self, repo: LibraryRepository | None = None) -> None:
        self._repo = repo or LibraryRepository()

    def register_project(self, path: str, title: str | None = None, tags: str = "") -> int:
        path = os.path.abspath(path)
        if title is None:
            title = os.path.splitext(os.path.basename(path))[0]
        model = LibraryProject(
            id=None,
            title=title,
            project_path=path,
            tags=tags,
            thumbnail=None,
            last_opened_at=None,
            created_at=None,
            db_version=None,
            archived=0,
        )
        return self._repo.upsert_project(model)

    def search(self, query: str = "", include_archived: bool = False) -> List[LibraryProject]:
        return self._repo.list_projects(query=query, include_archived=include_archived)

    def archive(self, path: str, archived: bool = True) -> None:
        self._repo.archive(path, archived=archived)

    def remove(self, path: str) -> None:
        self._repo.remove(path)

    def mark_opened(self, path: str) -> None:
        self._repo.mark_opened_now(path)


