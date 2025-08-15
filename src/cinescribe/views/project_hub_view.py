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
    QLineEdit,
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

        root = QVBoxLayout(self)
        root.setContentsMargins(12, 12, 12, 12)

        # 프로젝트 메타데이터 섹션
        meta_section = QVBoxLayout()
        meta_section.addWidget(QLabel("프로젝트 정보"))
        
        # 제목 편집
        title_row = QHBoxLayout()
        title_row.addWidget(QLabel("제목:"))
        self._title_edit = QLineEdit()
        self._title_edit.setPlaceholderText("프로젝트 제목...")
        title_row.addWidget(self._title_edit, 1)
        btn_title_save = QPushButton("제목 저장")
        title_row.addWidget(btn_title_save)
        meta_section.addLayout(title_row)
        
        # 태그 편집
        tags_row = QHBoxLayout()
        tags_row.addWidget(QLabel("태그:"))
        self._tags_edit = QLineEdit()
        self._tags_edit.setPlaceholderText("태그1, 태그2, 태그3...")
        tags_row.addWidget(self._tags_edit, 1)
        btn_tags_save = QPushButton("태그 저장")
        tags_row.addWidget(btn_tags_save)
        meta_section.addLayout(tags_row)
        
        root.addLayout(meta_section)
        
        # 구분선
        separator = QLabel("─" * 50)
        separator.setAlignment(Qt.AlignCenter)
        root.addWidget(separator)

        # 로그라인 편집 섹션
        logline_section = QVBoxLayout()
        logline_section.addWidget(QLabel("로그라인 (JSON)"))
        
        # 로그라인 툴바
        toolbar = QHBoxLayout()
        self._btn_load = QPushButton("불러오기")
        self._btn_save = QPushButton("저장")
        self._btn_export = QPushButton("내보내기")
        toolbar.addWidget(self._btn_load)
        toolbar.addWidget(self._btn_save)
        toolbar.addWidget(self._btn_export)
        logline_section.addLayout(toolbar)

        self._editor = QTextEdit()
        self._editor.setPlaceholderText("여기에 JSON을 입력하세요…")
        self._editor.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        try:
            self._editor.setLineWrapMode(QTextEdit.NoWrap)
        except Exception:
            pass
        self._apply_text_contrast()
        logline_section.addWidget(self._editor)
        
        root.addLayout(logline_section)

        self._status = QLabel("")
        self._status.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        root.addWidget(self._status)

        # 이벤트 연결
        btn_title_save.clicked.connect(self._on_save_title)
        btn_tags_save.clicked.connect(self._on_save_tags)
        self._btn_load.clicked.connect(self._on_load)
        self._btn_save.clicked.connect(self._on_save)
        self._btn_export.clicked.connect(self._on_export)

    def showEvent(self, event) -> None:  # type: ignore[override]
        super().showEvent(event)
        self._ensure_service()
        # 첫 표시 시에도 에디터가 비어있지 않도록 현재 키 데이터를 자동 로드
        try:
            self._on_load()
            self._load_project_meta()
        except Exception:
            pass

    def refresh(self) -> None:
        # 외부에서 호출 가능한 갱신 API: 서비스 보장 후 에디터 자동 로드
        self._ensure_service()
        try:
            self._on_load()
            self._load_project_meta()
        except Exception:
            pass

    def _ensure_service(self) -> None:
        db_path = get_current_project_path()
        if not db_path:
            self._status.setText("프로젝트가 열려 있지 않습니다. 라이브러리에서 프로젝트를 열어주세요.")
            self._editor.setEnabled(False)
            self._btn_load.setEnabled(False)
            self._btn_save.setEnabled(False)
            self._btn_export.setEnabled(False)
            self._title_edit.setEnabled(False)
            self._tags_edit.setEnabled(False)
            return
        if self._doc_service is None or self._doc_service._repo._db_path != db_path:
            self._doc_service = DocumentService(db_path)
        if self._project_service is None or self._project_service._repo._db_path != db_path:
            self._project_service = ProjectService(db_path)
        self._editor.setEnabled(True)
        self._btn_load.setEnabled(True)
        self._btn_save.setEnabled(True)
        self._btn_export.setEnabled(True)
        self._title_edit.setEnabled(True)
        self._tags_edit.setEnabled(True)
        self._status.setText(f"현재 프로젝트: {db_path}")
        self._apply_text_contrast()

    def _load_project_meta(self) -> None:
        """프로젝트 메타데이터 로드"""
        if not self._project_service:
            return
        try:
            info = self._project_service.load_info()
            if info:
                self._title_edit.setText(info.title or "")
                self._tags_edit.setText(info.tags or "")
        except Exception as e:
            print(f"프로젝트 메타데이터 로드 실패: {e}")

    def _on_save_title(self) -> None:
        """프로젝트 제목 저장"""
        if not self._project_service:
            return
        try:
            title = self._title_edit.text().strip()
            self._project_service.update_title(title)
            self._status.setText("제목 저장 완료")
        except Exception as e:
            self._status.setText(f"제목 저장 실패: {e}")

    def _on_save_tags(self) -> None:
        """프로젝트 태그 저장"""
        if not self._project_service:
            return
        try:
            tags = self._tags_edit.text().strip()
            self._project_service.update_tags(tags)
            self._status.setText("태그 저장 완료")
        except Exception as e:
            self._status.setText(f"태그 저장 실패: {e}")

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