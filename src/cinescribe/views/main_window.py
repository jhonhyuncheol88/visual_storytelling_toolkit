from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QTabWidget,
)

from .project_library_view import ProjectLibraryView
from .project_hub_view import ProjectHubView
from .visual_prompt_view import VisualPromptView
from .cinematic_view import CinematicView
from .storyboard_view import StoryboardView
from .final_images_view import FinalImagesView
from .audio_view import AudioView
from .characters_view import CharactersView
from .assets_view import AssetsView
from ..utils.app_state import get_current_project_path
from ..service.library_service import LibraryService


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("ShotCanvas")
        self.resize(1200, 800)

        self._project_library_view = ProjectLibraryView()
        self._project_hub_view = ProjectHubView()
        self._visual_prompt_view = VisualPromptView()
        self._cinematic_view = CinematicView()
        self._storyboard_view = StoryboardView()
        self._final_images_view = FinalImagesView()
        self._audio_view = AudioView()
        self._characters_view = CharactersView()
        self._assets_view = AssetsView()

        # Left tab bar (West) + content handled by QTabWidget
        self._tabs = QTabWidget()
        # 상단 행(Row) 탭바
        self._tabs.setTabPosition(QTabWidget.North)
        self._tabs.setMovable(False)
        self._tabs.setDocumentMode(True)
        try:
            self._tabs.tabBar().setMinimumHeight(36)
        except Exception:
            pass

        # 창 제목을 현재 프로젝트에 맞춰 동기화하는 타이머/훅은 단순화를 위해 focus 이벤트에서 처리
        self._library_service = LibraryService()

        self.setCentralWidget(self._tabs)

        # Start in library-only mode
        self.enter_library_mode()

    def focusInEvent(self, event) -> None:  # type: ignore[override]
        super().focusInEvent(event)
        path = get_current_project_path()
        base_title = "ShotCanvas"
        if path:
            self.setWindowTitle(f"{base_title} — {path}")
        else:
            self.setWindowTitle(base_title)

    def mark_project_opened(self) -> None:
        path = get_current_project_path()
        if path:
            self._library_service.mark_opened(path)

    def enter_library_mode(self) -> None:
        # Only show the Project Library as a single tab
        self._tabs.clear()
        self._tabs.addTab(self._project_library_view, "프로젝트 관리")
        self.setWindowTitle("ShotCanvas")

    def enter_project_mode(self) -> None:
        # Build project tabs: Back + modules
        self._tabs.clear()
        self._tabs.addTab(QWidget(), "뒤로가기")
        self._tabs.addTab(self._project_hub_view, "로그라인")
        self._tabs.addTab(self._visual_prompt_view, "비쥬얼")
        self._tabs.addTab(self._cinematic_view, "시네마틱")
        self._tabs.addTab(self._storyboard_view, "스토리보드")
        self._tabs.addTab(self._final_images_view, "최종 이미지")
        self._tabs.addTab(self._audio_view, "오디오")
        self._tabs.addTab(self._characters_view, "캐릭터")
        self._tabs.addTab(self._assets_view, "에셋")
        self._tabs.setCurrentIndex(1)
        # Hook tab change for back behavior
        self._tabs.currentChanged.connect(self._on_tabs_changed)
        # mark opened and update title
        self.mark_project_opened()
        self.focusInEvent(None)  # refresh title

    def _on_tabs_changed(self, index: int) -> None:
        if index == 0:
            # Back to project library
            try:
                self._tabs.currentChanged.disconnect(self._on_tabs_changed)
            except Exception:
                pass
            self.enter_library_mode()


