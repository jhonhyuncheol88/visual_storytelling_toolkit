from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QTextEdit,
    QPushButton,
    QFileDialog,
    QSizePolicy,
)
from PySide6.QtGui import QPalette, QColor

from ..utils.app_state import get_current_project_path
from ..repository.audio_repository import AudioRepository
import json as _json


class AudioView(QWidget):
    """오디오 보드 편집 화면.

    ProjectHubView와 유사하게 단일 JSON(Text) 문서를 편집/저장/내보내기한다.
    저장은 프로젝트 DB 내 AudioBoard 테이블(단일 행)에 기록된다.
    """

    def __init__(self) -> None:
        super().__init__()

        self._repo: AudioRepository | None = None

        root = QVBoxLayout(self)
        root.setContentsMargins(12, 12, 12, 12)

        toolbar = QHBoxLayout()
        title = QLabel("오디오 (JSON)")
        self._btn_load = QPushButton("불러오기")
        self._btn_save = QPushButton("저장")
        self._btn_export = QPushButton("내보내기")
        toolbar.addWidget(title)
        toolbar.addWidget(self._btn_load)
        toolbar.addWidget(self._btn_save)
        toolbar.addWidget(self._btn_export)

        self._editor = QTextEdit()
        self._editor.setPlaceholderText("오디오 보드용 JSON 코드를 입력하세요…")
        self._editor.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        try:
            self._editor.setLineWrapMode(QTextEdit.NoWrap)
        except Exception:
            pass
        self._apply_text_contrast()

        self._status = QLabel("")
        self._status.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        root.addLayout(toolbar)
        root.addWidget(self._editor)
        root.addWidget(self._status)

        self._btn_load.clicked.connect(self._on_load)
        self._btn_save.clicked.connect(self._on_save)
        self._btn_export.clicked.connect(self._on_export)

    def showEvent(self, event) -> None:  # type: ignore[override]
        super().showEvent(event)
        self._ensure_repo()
        # 첫 표시 시에도 에디터가 비어있지 않도록 현재 키 데이터를 자동 로드
        try:
            self._on_load()
        except Exception:
            pass

    def refresh(self) -> None:
        # 외부에서 호출 가능한 갱신 API: 서비스 보장 후 에디터 자동 로드
        self._ensure_repo()
        try:
            self._on_load()
        except Exception:
            pass

    def _ensure_repo(self) -> None:
        db_path = get_current_project_path()
        if not db_path:
            self._status.setText("프로젝트가 열려 있지 않습니다. 라이브러리에서 프로젝트를 열어주세요.")
            self._editor.setEnabled(True)
            self._btn_load.setEnabled(False)
            self._btn_save.setEnabled(False)
            self._btn_export.setEnabled(False)
            return
        if self._repo is None or self._repo._db_path != db_path:
            self._repo = AudioRepository(db_path)
        self._editor.setEnabled(True)
        self._btn_load.setEnabled(True)
        self._btn_save.setEnabled(True)
        self._btn_export.setEnabled(True)
        self._status.setText(f"현재 프로젝트: {db_path}")
        self._apply_text_contrast()

    def _on_load(self) -> None:
        self._ensure_repo()
        if not self._repo:
            return
        board = self._repo.get()
        if board is None:
            self._editor.setPlainText("")
        else:
            if board.format == "json":
                try:
                    data = _json.loads(board.content)
                    self._editor.setPlainText(_json.dumps(data, ensure_ascii=False, indent=2))
                except Exception:
                    self._editor.setPlainText(board.content)
            else:
                self._editor.setPlainText(board.content)
        self._status.setText("불러오기 완료: 오디오 보드")

    def _on_save(self) -> None:
        self._ensure_repo()
        if not self._repo:
            return
        content = self._editor.toPlainText()
        # JSON 우선 저장
        try:
            data = _json.loads(content) if content.strip() else {}
            self._repo.upsert("json", _json.dumps(data, ensure_ascii=False))
            self._status.setText("저장 완료: 오디오 보드(JSON)")
        except Exception:
            # JSON 파싱 실패 시 text로 저장
            self._repo.upsert("text", content)
            self._status.setText("저장 완료: 오디오 보드(Text)")

    def _on_export(self) -> None:
        self._ensure_repo()
        if not self._repo:
            return
        default_name = "audio_board.json"
        path, _ = QFileDialog.getSaveFileName(self, "내보내기", default_name, "JSON (*.json);;Text (*.txt)")
        if not path:
            return
        try:
            self._repo.export_to_file(path)
            self._status.setText(f"내보내기 완료: {path}")
        except Exception as e:
            self._status.setText(f"내보내기 실패: {e}")

    def _apply_text_contrast(self) -> None:
        try:
            bg = self._editor.palette().color(QPalette.Base)
            luma = 0.2126 * bg.red() + 0.7152 * bg.green() + 0.0722 * bg.blue()
            fg = QColor("#f0f0f0" if luma < 128 else "#202020")
            pal = self._editor.palette()
            pal.setColor(QPalette.Text, fg)
            self._editor.setPalette(pal)
        except Exception:
            pass


