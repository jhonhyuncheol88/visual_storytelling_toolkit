from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame


class ProjectCard(QFrame):
    def __init__(self, title: str, path: str, tags: str = "", last_opened_at: str | None = None) -> None:
        super().__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setProperty("class", "project-card")

        root = QVBoxLayout(self)

        title_lbl = QLabel(title)
        title_lbl.setProperty("class", "card-title")
        title_lbl.setTextInteractionFlags(Qt.TextSelectableByMouse)

        path_lbl = QLabel(path)
        path_lbl.setProperty("class", "card-path")
        path_lbl.setTextInteractionFlags(Qt.TextSelectableByMouse)

        info_row = QHBoxLayout()
        tags_lbl = QLabel(f"# {tags}" if tags else "# (no-tags)")
        tags_lbl.setProperty("class", "card-tags")
        last_lbl = QLabel(last_opened_at or "최근 열람 기록 없음")
        last_lbl.setProperty("class", "card-last-opened")
        info_row.addWidget(tags_lbl)
        info_row.addStretch(1)
        info_row.addWidget(last_lbl)

        root.addWidget(title_lbl)
        root.addWidget(path_lbl)
        root.addLayout(info_row)


