from __future__ import annotations

from typing import Optional

_current_project_path: Optional[str] = None


def set_current_project_path(path: Optional[str]) -> None:
    global _current_project_path
    _current_project_path = path


def get_current_project_path() -> Optional[str]:
    return _current_project_path


def require_current_project_path() -> str:
    if not _current_project_path:
        raise RuntimeError("No project opened")
    return _current_project_path


