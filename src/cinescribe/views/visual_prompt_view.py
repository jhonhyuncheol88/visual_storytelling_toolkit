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


class VisualPromptView(QWidget):
    """비쥬얼 프롬프트(JSON) 편집/저장 화면.

    ProjectHubView와 동일한 구성으로, Documents 테이블의
    key='visual_prompt' 항목을 JSON 형식으로 저장/불러오기/내보내기한다.
    """

    _DOC_KEY = "visual_prompt"

    def __init__(self) -> None:
        super().__init__()

        self._doc_service: DocumentService | None = None

        root = QVBoxLayout(self)
        root.setContentsMargins(12, 12, 12, 12)

        toolbar = QHBoxLayout()
        title = QLabel("비쥬얼 프롬프트 (JSON)")
        self._btn_load = QPushButton("불러오기")
        self._btn_save = QPushButton("저장")
        self._btn_export = QPushButton("내보내기")
        toolbar.addWidget(title)
        toolbar.addWidget(self._btn_load)
        toolbar.addWidget(self._btn_save)
        toolbar.addWidget(self._btn_export)

        self._editor = QTextEdit()
        self._editor.setPlaceholderText("비쥬얼 프롬프트용 JSON 코드를 입력하세요…")
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
            self._editor.setEnabled(True)
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
        data = self._doc_service.load_json(self._DOC_KEY)
        import json as _json
        if data is None:
            self._editor.setPlainText("")
        else:
            # 데이터 타입에 따라 다르게 표시
            if isinstance(data, dict) and "type" in data and data["type"] == "text":
                # 텍스트 형식이면 content만 표시
                self._editor.setPlainText(data.get("content", ""))
            else:
                # JSON 형식이면 포맷팅해서 표시
                self._editor.setPlainText(_json.dumps(data, ensure_ascii=False, indent=2))
        self._status.setText("불러오기 완료: 비쥬얼 프롬프트")

    def _on_save(self) -> None:
        self._ensure_service()
        if not self._doc_service:
            return
        content = self._editor.toPlainText()
        try:
            import json as _json

            # 텍스트 내용을 그대로 저장 (JSON 강제 아님)
            if not content.strip():
                # 빈 내용이면 빈 객체로 저장
                data = {}
            else:
                # JSON 형식인지 확인
                try:
                    data = _json.loads(content)
                    # JSON 형식이면 파싱된 데이터로 저장
                    print("JSON 형식으로 저장됨")
                except _json.JSONDecodeError:
                    # JSON이 아니면 텍스트로 저장
                    data = {"content": content, "type": "text"}
                    print("텍스트 형식으로 저장됨")
            
            # 데이터 저장
            self._doc_service.save_json(self._DOC_KEY, data)
            self._status.setText("저장 완료: 비쥬얼 프롬프트")
            
        except Exception as e:
            # 더 자세한 오류 정보 표시
            import traceback
            error_details = f"저장 실패: {e}\n{traceback.format_exc()}"
            self._status.setText(error_details)
            print(f"VisualPromptView 저장 오류: {error_details}")

    def _on_export(self) -> None:
        self._ensure_service()
        if not self._doc_service:
            return
        default_name = f"{self._DOC_KEY}.json"
        path, _ = QFileDialog.getSaveFileName(self, "내보내기", default_name, "JSON (*.json);")
        if not path:
            return
        try:
            self._doc_service.export(self._DOC_KEY, path)
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


