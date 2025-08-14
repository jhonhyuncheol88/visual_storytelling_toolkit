from __future__ import annotations

import json
from typing import Any, Optional

from ..repository.document_repository import DocumentRepository, Document


class DocumentService:
    def __init__(self, db_path: str) -> None:
        self._repo = DocumentRepository(db_path)

    def save_text(self, key: str, text: str) -> int:
        return self._repo.upsert(Document(id=None, key=key, format="text", content=text))

    def save_json(self, key: str, data: Any) -> int:
        content = json.dumps(data, ensure_ascii=False)
        return self._repo.upsert(Document(id=None, key=key, format="json", content=content))

    def load_text(self, key: str) -> Optional[str]:
        doc = self._repo.get(key)
        if not doc:
            return None
        return doc.content

    def load_json(self, key: str) -> Optional[Any]:
        doc = self._repo.get(key)
        if not doc:
            return None
        try:
            return json.loads(doc.content)
        except Exception:
            return None

    def export(self, key: str, out_path: str) -> None:
        self._repo.export_to_file(key, out_path)


