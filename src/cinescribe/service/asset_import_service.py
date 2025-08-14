from __future__ import annotations

import hashlib
import os
import shutil
from pathlib import Path
from typing import Optional, Tuple

from PIL import Image

from ..utils.project_paths import get_project_dirs
from ..repository.asset_repository import AssetRepository


class AssetImportService:
    def __init__(self, db_path: str) -> None:
        self._db_path = db_path
        self._assets_dir, self._thumbs_dir = get_project_dirs(db_path)
        self._asset_repo = AssetRepository(db_path)

    def import_image(self, src_path: str) -> Tuple[int, str, str]:
        # Returns (asset_id, project_relative_path, thumbnail_relative_path)
        src_path = os.path.abspath(src_path)
        with open(src_path, "rb") as f:
            content = f.read()
        sha = hashlib.sha256(content).hexdigest()
        ext = os.path.splitext(src_path)[1].lower()
        filename = f"{sha}{ext}"
        dest_path = os.path.join(self._assets_dir, filename)
        if not os.path.exists(dest_path):
            shutil.copy2(src_path, dest_path)
        # thumbnail
        thumb_name = f"{sha}_thumb.jpg"
        thumb_path = os.path.join(self._thumbs_dir, thumb_name)
        if not os.path.exists(thumb_path):
            img = Image.open(dest_path)
            img.thumbnail((512, 512))
            img.convert("RGB").save(thumb_path, quality=85)
        # Return relative paths (relative to assets dir base)
        proj_rel = os.path.relpath(dest_path, os.path.dirname(self._db_path))
        thumb_rel = os.path.relpath(thumb_path, os.path.dirname(self._db_path))
        # Record in Assets table
        width = height = None
        try:
            with Image.open(dest_path) as im:
                width, height = im.size
        except Exception:
            pass
        asset_id = self._asset_repo.upsert_image(
            original_path=src_path,
            project_path=proj_rel,
            filename=filename,
            ext=ext,
            width=width,
            height=height,
            hash_sha256=sha,
            thumbnail_path=thumb_rel,
        )
        return asset_id, proj_rel, thumb_rel


