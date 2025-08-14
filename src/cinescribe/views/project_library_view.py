from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QHBoxLayout,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QFileDialog,
    QMenu,
    QMessageBox,
)

from ..service.library_service import LibraryService
from ..service.project_init_service import ProjectInitService
from ..utils.app_state import set_current_project_path
from .project_hub_view import ProjectHubView
from ..widgets.project_card import ProjectCard


class ProjectLibraryView(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._service = LibraryService()
        self._project_init = ProjectInitService()

        root = QVBoxLayout(self)

        # Toolbar
        toolbar = QHBoxLayout()
        self._search = QLineEdit()
        self._search.setPlaceholderText("검색: 제목/태그")
        btn_new = QPushButton("새 프로젝트")
        btn_add = QPushButton("기존 추가")
        toolbar.addWidget(self._search)
        toolbar.addWidget(btn_new)
        toolbar.addWidget(btn_add)

        # List
        self._list = QListWidget()
        self._list.setContextMenuPolicy(Qt.CustomContextMenu)
        self._empty_label = QLabel("등록된 프로젝트가 없습니다.")
        self._empty_label.setAlignment(Qt.AlignCenter)

        root.addLayout(toolbar)
        root.addWidget(self._list)
        root.addWidget(self._empty_label)

        self._search.textChanged.connect(self._refresh)
        btn_add.clicked.connect(self._on_add_existing)
        btn_new.clicked.connect(self._on_create_new)
        self._list.itemDoubleClicked.connect(self._on_open_project)
        self._list.customContextMenuRequested.connect(self._on_context_menu)

        self._refresh()

    def _refresh(self) -> None:
        query = self._search.text().strip()
        projects = self._service.search(query=query)
        self._list.clear()
        for p in projects:
            card = ProjectCard(title=p.title, path=p.project_path, tags=p.tags or "", last_opened_at=p.last_opened_at)
            item = QListWidgetItem(self._list)
            item.setData(Qt.UserRole, p.project_path)
            item.setSizeHint(card.sizeHint())
            self._list.addItem(item)
            self._list.setItemWidget(item, card)
        self._empty_label.setVisible(self._list.count() == 0)

    def _on_add_existing(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "프로젝트 파일 선택", "", "CineScribe (*.cinescribe);;SQLite (*.sqlite *.db);;All Files (*)")
        if not path:
            return
        self._service.register_project(path)
        self._refresh()

    def _on_create_new(self) -> None:
        path, _ = QFileDialog.getSaveFileName(self, "새 프로젝트 저장 위치", "untitled.cinescribe", "CineScribe (*.cinescribe)")
        if not path:
            return
        self._project_init.create_new_project(path)
        self._service.register_project(path)
        self._refresh()

    def _on_open_project(self) -> None:
        item = self._list.currentItem()
        if not item:
            return
        path = item.data(Qt.UserRole)
        set_current_project_path(path)
        # 메인 윈도우의 스택에서 Project Hub로 전환
        # 부모가 MainWindow 구조를 갖고 있으므로, 약한 참조로 상위 위젯을 탐색합니다.
        w = self.parent()
        while w and not hasattr(w, "parent") and not hasattr(w, "setWindowTitle"):
            w = w.parent()
        # 안전하게 스택 전환: MainWindow가 인덱스 1이 Project Hub라는 계약을 가짐
        # 더 견고한 전환은 신호를 사용해 MainWindow가 처리하도록 개선 예정
        try:
            from .main_window import MainWindow  # lazy import

            mw = self.window()
            if hasattr(mw, "enter_project_mode"):
                mw.enter_project_mode()
        except Exception:
            pass

    def _on_context_menu(self, pos) -> None:
        item = self._list.itemAt(pos)
        if not item:
            return
        path = item.data(Qt.UserRole)
        menu = QMenu(self)
        act_remove = menu.addAction("라이브러리에서 제거")
        act_delete = menu.addAction("디스크에서 삭제")
        act = menu.exec(self._list.mapToGlobal(pos))
        if act == act_remove:
            self._remove_from_library(path)
        elif act == act_delete:
            self._delete_from_disk(path)

    def _remove_from_library(self, path: str) -> None:
        self._service.remove(path)
        self._refresh()

    def _delete_from_disk(self, path: str) -> None:
        reply = QMessageBox.question(
            self,
            "디스크에서 삭제",
            f"선택한 프로젝트 파일을 디스크에서 삭제할까요?\n{path}",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply != QMessageBox.Yes:
            return
        import os
        try:
            if os.path.exists(path):
                os.remove(path)
        except Exception:
            pass
        finally:
            self._service.remove(path)
            self._refresh()


