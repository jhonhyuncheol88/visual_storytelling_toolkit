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
from ..service.document_service import DocumentService
from ..service.project_service import ProjectService


class ProjectHubView(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self._doc_service: DocumentService | None = None
        self._project_service: ProjectService | None = None
        # Simplified: no gallery/images in Hub

        root = QVBoxLayout(self)

        # Layout margins to avoid tabbar clipping
        root.setContentsMargins(12, 12, 12, 12)

        # Toolbar (로그라인 JSON 전용)
        toolbar = QHBoxLayout()
        title = QLabel("로그라인 (JSON)")
        self._btn_load = QPushButton("불러오기")
        self._btn_save = QPushButton("저장")
        self._btn_export = QPushButton("내보내기")
        toolbar.addWidget(title)
        toolbar.addWidget(self._btn_load)
        toolbar.addWidget(self._btn_save)
        toolbar.addWidget(self._btn_export)

        self._editor = QTextEdit()
        self._editor.setPlaceholderText("여기에 텍스트 또는 JSON을 입력하세요…")
        self._editor.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        try:
            self._editor.setLineWrapMode(QTextEdit.NoWrap)
        except Exception:
            pass
        # Apply high-contrast text color for dark/light themes
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
        self._ensure_service()
        # 첫 표시 시에도 에디터가 비어있지 않도록 현재 키 데이터를 자동 로드
        try:
            self._on_load()
        except Exception:
            pass

    def refresh(self) -> None:
        # 외부에서 호출 가능한 갱신 API: 서비스 보장 후 에디터 자동 로드
        self._ensure_service()
        try:
            self._on_load()
        except Exception:
            pass

    def _ensure_service(self) -> None:
        db_path = get_current_project_path()
        if not db_path:
            self._status.setText("프로젝트가 열려 있지 않습니다. 라이브러리에서 프로젝트를 열어주세요.")
            # 에디터는 항상 입력 가능하게 유지
            self._editor.setEnabled(True)
            # 파일 연동 버튼만 비활성화
            self._btn_load.setEnabled(False)
            self._btn_save.setEnabled(False)
            self._btn_export.setEnabled(False)
            return
        if self._doc_service is None or self._doc_service._repo._db_path != db_path:
            self._doc_service = DocumentService(db_path)
        self._editor.setEnabled(True)
        self._btn_load.setEnabled(True)
        self._btn_save.setEnabled(True)
        self._btn_export.setEnabled(True)
        self._status.setText(f"현재 프로젝트: {db_path}")
        self._apply_text_contrast()

    def _on_load(self) -> None:
        self._ensure_service()
        if not self._doc_service:
            return
        # Always use 'logline' JSON
        data = self._doc_service.load_json("logline")
        import json as _json
        if data is None:
            self._editor.setPlainText("{}")
        else:
            self._editor.setPlainText(_json.dumps(data, ensure_ascii=False, indent=2))
        self._status.setText("불러오기 완료: 로그라인")

    def _on_save(self) -> None:
        self._ensure_service()
        if not self._doc_service:
            return
        content = self._editor.toPlainText()
        try:
            import json as _json

            data = _json.loads(content) if content.strip() else {}
            self._doc_service.save_json("logline", data)
            self._status.setText("저장 완료: 로그라인")
        except Exception as e:
            self._status.setText(f"저장 실패: {e}")

    def _on_export(self) -> None:
        self._ensure_service()
        if not self._doc_service:
            return
        default_name = "logline.json"
        path, _ = QFileDialog.getSaveFileName(self, "내보내기", default_name, "JSON (*.json);")
        if not path:
            return
        try:
            self._doc_service.export("logline", path)
            self._status.setText(f"내보내기 완료: {path}")
        except Exception as e:
            self._status.setText(f"내보내기 실패: {e}")




    def _apply_text_contrast(self) -> None:
        # Adjust editor text color based on background brightness
        try:
            bg = self._editor.palette().color(QPalette.Base)
            luma = 0.2126 * bg.red() + 0.7152 * bg.green() + 0.0722 * bg.blue()
            fg = QColor("#f0f0f0" if luma < 128 else "#202020")
            pal = self._editor.palette()
            pal.setColor(QPalette.Text, fg)
            self._editor.setPalette(pal)
        except Exception:
            pass