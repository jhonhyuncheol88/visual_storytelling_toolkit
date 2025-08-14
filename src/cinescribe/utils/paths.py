from __future__ import annotations

import os
from pathlib import Path


def get_app_data_dir() -> str:
    home = Path(os.path.expanduser("~"))
    app_dir = home / ".cinescribe"
    app_dir.mkdir(parents=True, exist_ok=True)
    return str(app_dir)


def get_library_db_path() -> str:
    app_dir = get_app_data_dir()
    return str(Path(app_dir) / "library.sqlite")


def ensure_dir(path: str) -> None:
    Path(path).mkdir(parents=True, exist_ok=True)


