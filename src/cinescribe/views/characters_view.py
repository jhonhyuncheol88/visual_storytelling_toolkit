from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QTextEdit,
    QLineEdit,
    QFileDialog,
)

from ..utils.app_state import get_current_project_path
from ..repository.character_repository import CharacterRepository
from ..service.asset_import_service import AssetImportService
from ..repository.asset_repository import AssetRepository


class CharactersView(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._repo: CharacterRepository | None = None
        self._asset_service: AssetImportService | None = None

        root = QVBoxLayout(self)

        toolbar = QHBoxLayout()
        btn_new = QPushButton("캐릭터 추가")
        btn_del = QPushButton("삭제")
        toolbar.addWidget(btn_new)
        toolbar.addWidget(btn_del)

        content = QHBoxLayout()
        self._list = QListWidget()
        self._list.setMinimumWidth(260)

        right = QVBoxLayout()
        # 섹션 1: 캐릭터 이름
        right.addWidget(QLabel("이름"))
        self._name = QLineEdit()
        self._name.setPlaceholderText("캐릭터 이름…")
        right.addWidget(self._name)

        # 섹션 2: 이미지 임포트 + 미리보기
        right.addWidget(QLabel("이미지"))
        self._img_label = QLabel("이미지 미리보기 없음")
        self._img_label.setAlignment(Qt.AlignCenter)
        self._img_label.setMinimumSize(320, 180)
        self._img_label.setStyleSheet("QLabel{border:1px solid #888;}")
        right.addWidget(self._img_label)
        btn_img = QPushButton("이미지 임포트")
        btn_img_remove = QPushButton("이미지 제거")
        right.addWidget(btn_img)
        right.addWidget(btn_img_remove)

        # 섹션 3: 디자인 프롬프트
        right.addWidget(QLabel("디자인 프롬프트"))
        self._design_prompt = QTextEdit()
        self._design_prompt.setPlaceholderText("디자인 프롬프트…")
        right.addWidget(self._design_prompt, 1)
        btn_save = QPushButton("저장")
        right.addWidget(btn_save)

        content.addWidget(self._list)
        content.addLayout(right)

        root.addLayout(toolbar)
        root.addLayout(content)
        # 상태 표시
        self._status = QLabel("")
        self._status.setWordWrap(True)
        root.addWidget(self._status)

        self._list.currentItemChanged.connect(self._on_select)
        btn_new.clicked.connect(self._on_new)
        btn_del.clicked.connect(self._on_delete)
        btn_save.clicked.connect(self._on_save)
        btn_img.clicked.connect(self._on_set_image)
        btn_img_remove.clicked.connect(self._on_remove_image)

        self._refresh()

    def showEvent(self, event) -> None:  # type: ignore[override]
        try:
            super().showEvent(event)
        except Exception:
            pass
        self._refresh()

    def refresh(self) -> None:
        # 외부에서 호출 가능한 갱신 API
        self._ensure()
        self._refresh_shots()

    def _ensure(self) -> None:
        db_path = get_current_project_path()
        if not db_path:
            return
        if self._repo is None or self._repo._db_path != db_path:
            self._repo = CharacterRepository(db_path)
            self._asset_service = AssetImportService(db_path)

    def _refresh(self) -> None:
        self._ensure()
        if not self._repo:
            return
        self._list.clear()
        from PySide6.QtGui import QIcon, QPixmap
        import os
        db_path = get_current_project_path()
        project_dir = os.path.dirname(db_path) if db_path else None
        for c in self._repo.list_characters():
            it = QListWidgetItem(c.name)
            it.setData(Qt.UserRole, c.id)
            if c.image_asset_id and project_dir:
                from ..repository.asset_repository import AssetRepository
                a = AssetRepository(db_path).get_by_id(c.image_asset_id)
                p: str | None = None
                if a and a.thumbnail_path:
                    t = os.path.join(project_dir, a.thumbnail_path)
                    if os.path.exists(t):
                        p = t
                if not p and a and a.project_path:
                    t2 = os.path.join(project_dir, a.project_path)
                    if os.path.exists(t2):
                        p = t2
                if p:
                    it.setIcon(QIcon(QPixmap(p)))
            self._list.addItem(it)

    def _on_select(self) -> None:
        if not self._repo:
            return
        it = self._list.currentItem()
        if not it:
            return
        c = self._repo.get(int(it.data(Qt.UserRole)))
        if not c:
            return
        self._name.setText(c.name)
        self._design_prompt.setPlainText(c.design_prompt or "")
        # 이미지 미리보기 업데이트
        from PySide6.QtGui import QPixmap
        import os
        self._img_label.setText("이미지 미리보기 없음")
        db_path = get_current_project_path()
        if db_path and c.image_asset_id:
            from ..repository.asset_repository import AssetRepository
            a = AssetRepository(db_path).get_by_id(c.image_asset_id)
            p: str | None = None
            if a and a.thumbnail_path:
                t = os.path.join(os.path.dirname(db_path), a.thumbnail_path)
                if os.path.exists(t):
                    p = t
            if not p and a and a.project_path:
                t2 = os.path.join(os.path.dirname(db_path), a.project_path)
                if os.path.exists(t2):
                    p = t2
            if p:
                pix = QPixmap(p)
                if not pix.isNull():
                    self._img_label.setPixmap(pix.scaled(self._img_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def _on_new(self) -> None:
        self._ensure()
        if not self._repo:
            return
        new_id = self._repo.create("새 캐릭터")
        self._refresh()
        # select new
        for i in range(self._list.count()):
            if int(self._list.item(i).data(Qt.UserRole)) == new_id:
                self._list.setCurrentRow(i)
                break

    def _on_delete(self) -> None:
        if not self._repo:
            return
        it = self._list.currentItem()
        if not it:
            return
        self._repo.delete(int(it.data(Qt.UserRole)))
        self._refresh()

    def _on_save(self) -> None:
        if not self._repo:
            return
        it = self._list.currentItem()
        if not it:
            return
        cid = int(it.data(Qt.UserRole))
        self._repo.update(
            cid,
            name=self._name.text().strip(),
            design_prompt=self._design_prompt.toPlainText().strip(),
        )
        # 목록 표시 이름 즉시 갱신
        new_name = self._name.text().strip() or "(이름 없음)"
        it.setText(new_name)

    def _on_set_image(self) -> None:
        if not self._asset_service or not self._repo:
            self._status.setText("프로젝트가 열려 있지 않습니다.")
            return
        it = self._list.currentItem()
        if not it:
            self._status.setText("캐릭터를 선택하세요.")
            return
        path, _ = QFileDialog.getOpenFileName(self, "캐릭터 이미지", "", "Images (*.png *.jpg *.jpeg *.webp *.bmp);;All Files (*)")
        if not path:
            return
        try:
            cid = int(it.data(Qt.UserRole))
            asset_id, proj_rel, thumb_rel = self._asset_service.import_image(path)
            self._repo.link_image(cid, asset_id)
            # 우측 미리보기 & 좌측 아이콘 갱신, 선택 유지
            self._on_select()
            self._refresh()
            # restore selection
            for i in range(self._list.count()):
                if int(self._list.item(i).data(Qt.UserRole)) == cid:
                    self._list.setCurrentRow(i)
                    break
            self._status.setText("이미지 임포트 및 연결 완료")
        except Exception as e:
            self._status.setText(f"임포트 실패: {e}")

    def _on_remove_image(self) -> None:
        # 캐릭터에 연결된 이미지를 해제하고, 참조가 없다면 에셋도 삭제 옵션
        if not self._repo:
            self._status.setText("프로젝트가 열려 있지 않습니다.")
            return
        it = self._list.currentItem()
        if not it:
            self._status.setText("캐릭터를 선택하세요.")
            return
        cid = int(it.data(Qt.UserRole))
        # 현재 캐릭터 조회
        c = self._repo.get(cid)
        if not c or not c.image_asset_id:
            self._status.setText("연결된 이미지가 없습니다.")
            return
        # 링크 해제
        self._repo.link_image(cid, None)
        # 에셋 참조 여부 확인 후 삭제 여부 묻기
        try:
            db_path = get_current_project_path()
            ar = AssetRepository(db_path) if db_path else None
            if ar and not ar.is_asset_referenced(c.image_asset_id):
                # 안전하게 파일은 남기고 DB 레코드만 제거
                ar.delete_asset(c.image_asset_id)
        except Exception:
            pass
        # UI 갱신
        self._img_label.clear()
        self._img_label.setText("이미지 미리보기 없음")
        self._refresh()
        # 선택 유지
        for i in range(self._list.count()):
            if int(self._list.item(i).data(Qt.UserRole)) == cid:
                self._list.setCurrentRow(i)
                break
        self._status.setText("이미지 연결 해제 완료")


