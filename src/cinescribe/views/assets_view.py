from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QLineEdit,
    QPushButton,
)

from ..utils.app_state import get_current_project_path
from ..repository.asset_repository import AssetRepository


class AssetsView(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._repo: AssetRepository | None = None

        root = QVBoxLayout(self)
        toolbar = QHBoxLayout()
        self._search = QLineEdit()
        self._search.setPlaceholderText("검색(tags/filename)")
        btn_refresh = QPushButton("새로고침")
        toolbar.addWidget(self._search)
        toolbar.addWidget(btn_refresh)

        self._list = QListWidget()

        root.addLayout(toolbar)
        root.addWidget(self._list)

        self._search.textChanged.connect(self._refresh)
        btn_refresh.clicked.connect(self._refresh)
        self._list.itemDoubleClicked.connect(self._on_edit_tags)
        self._refresh()

    def showEvent(self, event) -> None:  # type: ignore[override]
        # 탭 전환 등으로 화면에 표시될 때마다 최신 데이터로 새로고침
        try:
            super().showEvent(event)
        except Exception:
            pass
        self._refresh()

    def refresh(self) -> None:
        # 외부에서 호출 가능한 갱신 API
        self._ensure()
        self._refresh()

    def _ensure(self) -> None:
        db_path = get_current_project_path()
        if not db_path:
            return
        if self._repo is None or self._repo._db_path != db_path:
            self._repo = AssetRepository(db_path)

    def _refresh(self) -> None:
        self._ensure()
        if not self._repo:
            return
        # 간단 구현: 모든 이미지 에셋 리스트업
        from PySide6.QtGui import QIcon, QPixmap
        import os
        db_path = get_current_project_path()
        project_dir = os.path.dirname(db_path) if db_path else None
        self._list.clear()
        with self._repo._connect() as conn:
            q = self._search.text().strip()
            if q:
                rows = conn.execute(
                    "SELECT id, filename, project_path, thumbnail_path, tags FROM Assets WHERE kind='image' AND (tags LIKE ? OR filename LIKE ?) ORDER BY id DESC",
                    (f"%{q}%", f"%{q}%"),
                ).fetchall()
            else:
                rows = conn.execute("SELECT id, filename, project_path, thumbnail_path, tags FROM Assets WHERE kind='image' ORDER BY id DESC").fetchall()
            for r in rows:
                text = r["filename"]
                it = QListWidgetItem(text)
                it.setData(Qt.UserRole, r["id"])
                if project_dir and r["thumbnail_path"]:
                    p = os.path.join(project_dir, r["thumbnail_path"])
                    if os.path.exists(p):
                        it.setIcon(QIcon(QPixmap(p)))
                self._list.addItem(it)

    def _on_edit_tags(self) -> None:
        if not self._repo:
            return
        it = self._list.currentItem()
        if not it:
            return
        asset_id = int(it.data(Qt.UserRole))
        from PySide6.QtWidgets import QInputDialog

        ok = False
        with self._repo._connect() as conn:
            row = conn.execute("SELECT tags FROM Assets WHERE id=?", (asset_id,)).fetchone()
            current = row["tags"] if row else ""
        text, ok = QInputDialog.getText(self, "태그 편집", "태그(쉼표 구분)", text=current or "")
        if not ok:
            return
        self._repo.update_tags(asset_id, text)
        self._refresh()


