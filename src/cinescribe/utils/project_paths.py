from __future__ import annotations

import os
from pathlib import Path


def get_project_dirs(db_path: str) -> tuple[str, str]:
    base = Path(os.path.abspath(db_path))
    base_dir = base.parent
    stem = base.stem
    assets_dir = base_dir / f"{stem}_assets"
    thumbs_dir = assets_dir / "thumbnails"
    assets_dir.mkdir(parents=True, exist_ok=True)
    thumbs_dir.mkdir(parents=True, exist_ok=True)
    return str(assets_dir), str(thumbs_dir)


