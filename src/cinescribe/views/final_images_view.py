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
    QFileDialog,
    QMenu,
    QTextEdit,
)

from ..utils.app_state import get_current_project_path
from ..repository.final_image_repository import FinalImageRepository
from ..service.asset_import_service import AssetImportService
from PySide6.QtGui import QPalette, QColor, QBrush


class FinalImagesView(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self._repo: FinalImageRepository | None = None
        self._asset_service: AssetImportService | None = None
        self._current_scene_id: int | None = None

        root = QVBoxLayout(self)

        # Toolbar: simple actions (이미지 임포트만)
        toolbar = QHBoxLayout()
        btn_import_image = QPushButton("이미지 임포트")
        toolbar.addWidget(btn_import_image)

        # Shots grid(list for MVP)
        self._shots_list = QListWidget()
        self._shots_list.setResizeMode(QListWidget.Adjust)
        self._shots_list.setSpacing(8)
        self._shots_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self._shots_list.customContextMenuRequested.connect(self._on_context_menu)
        self._shots_list.setDragDropMode(QListWidget.InternalMove)
        self._shots_list.model().rowsMoved.connect(self._on_rows_moved)

        root.addLayout(toolbar)
        root.addWidget(self._shots_list)
        # status label
        self._status = QLabel("")
        self._status.setWordWrap(True)
        root.addWidget(self._status)

        btn_import_image.clicked.connect(self._on_import_image)

        self._ensure_repo()
        self._ensure_default_scene()
        self._refresh_scenes()
        self._apply_text_contrast()

    def showEvent(self, event) -> None:  # type: ignore[override]
        # 프로젝트 탭으로 진입할 때마다 저장소/장면 상태 갱신
        try:
            super().showEvent(event)
        except Exception:
            pass
        self._ensure_repo()
        self._ensure_default_scene()
        self._refresh_scenes()
        if hasattr(self, "_status"):
            self._status.setText("")

    def _apply_text_contrast(self) -> None:
        # 배경 밝기에 따라 리스트 텍스트 색상을 고대비로 설정
        bg = self._shots_list.palette().color(QPalette.Base)
        luma = 0.2126 * bg.red() + 0.7152 * bg.green() + 0.0722 * bg.blue()
        self._shot_text_qcolor = QColor("#f0f0f0" if luma < 128 else "#202020")
        self._shots_list.setStyleSheet(f"QListWidget {{ color: {self._shot_text_qcolor.name()}; }}")

    def _ensure_repo(self) -> None:
        db_path = get_current_project_path()
        if not db_path:
            return
        if self._repo is None or self._repo._db_path != db_path:
            self._repo = FinalImageRepository(db_path)
            self._asset_service = AssetImportService(db_path)

    def _ensure_default_scene(self) -> None:
        # 장면이 하나도 없으면 기본 장면을 자동 생성
        if not self._repo:
            return
        scenes = self._repo.list_scenes()
        if not scenes:
            try:
                self._repo.create_scene(number=1, name="기본 장면", notes="")
            except Exception:
                pass

    def _refresh_scenes(self) -> None:
        self._ensure_repo()
        if not self._repo:
            return
        scenes = self._repo.list_scenes()
        if scenes:
            self._current_scene_id = scenes[0].id
            self._refresh_shots()

    def _refresh_shots(self) -> None:
        if not self._repo or self._current_scene_id is None:
            return
        shots = self._repo.list_images(self._current_scene_id)
        self._shots_list.clear()
        from PySide6.QtGui import QPixmap
        import os

        project_dir = None
        db_path = get_current_project_path()
        if db_path:
            project_dir = os.path.dirname(db_path)

        for sh in shots:
            item = QListWidgetItem()
            item.setData(Qt.UserRole, sh.id)
            try:
                item.setForeground(QBrush(self._shot_text_qcolor))
            except Exception:
                pass

            # 이미지 경로
            thumb_abs = None
            if project_dir:
                if sh.asset_thumbnail_path:
                    t = os.path.join(project_dir, sh.asset_thumbnail_path)
                    if os.path.exists(t):
                        thumb_abs = t
                # 썸네일이 없으면 원본 경로로 폴백
                if not thumb_abs and getattr(sh, 'asset_project_path', None):
                    t2 = os.path.join(project_dir, sh.asset_project_path)
                    if os.path.exists(t2):
                        thumb_abs = t2

            # 위젯 구성: 이미지 + 메모 + 액션 버튼
            w = QWidget()
            row = QHBoxLayout(w)
            row.setContentsMargins(8, 8, 8, 8)
            img_label = QLabel()
            img_label.setFixedSize(200, 112)
            img_label.setAlignment(Qt.AlignCenter)
            if thumb_abs:
                try:
                    pix = QPixmap(thumb_abs)
                    if not pix.isNull():
                        img_label.setPixmap(pix.scaled(img_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
                except Exception:
                    pass
            memo = QTextEdit()
            memo.setPlaceholderText("메모…")
            memo.setPlainText(sh.description or "")
            memo.setFixedHeight(112)
            btns = QVBoxLayout()
            btn_save = QPushButton("저장")
            btn_replace = QPushButton("교체")
            btn_delete = QPushButton("삭제")
            btns.addWidget(btn_save)
            btns.addWidget(btn_replace)
            btns.addWidget(btn_delete)
            btns.addStretch(1)
            row.addWidget(img_label)
            row.addWidget(memo, 1)
            row.addLayout(btns)

            # 콜백 연결
            def do_save(shot_id: int, edit: QTextEdit) -> None:
                if not self._repo:
                    return
                self._repo.update_image_meta(shot_id, description=edit.toPlainText().strip())

            def do_replace(shot_id: int) -> None:
                if not self._asset_service or not self._repo:
                    return
                path, _ = QFileDialog.getOpenFileName(self, "이미지 선택", "", "Images (*.png *.jpg *.jpeg *.webp *.bmp);;All Files (*)")
                if not path:
                    return
                asset_id, proj_rel, thumb_rel = self._asset_service.import_image(path)
                self._repo.link_image_asset(shot_id, asset_id)
                self._refresh_shots()

            def do_delete(shot_id: int) -> None:
                if not self._repo:
                    return
                self._repo.delete_image(shot_id)
                self._refresh_shots()

            btn_save.clicked.connect(lambda _, sid=sh.id, e=memo: do_save(sid, e))
            btn_replace.clicked.connect(lambda _, sid=sh.id: do_replace(sid))
            btn_delete.clicked.connect(lambda _, sid=sh.id: do_delete(sid))

            item.setSizeHint(w.sizeHint())
            self._shots_list.addItem(item)
            self._shots_list.setItemWidget(item, w)

    def _on_context_menu(self, pos) -> None:
        item = self._shots_list.itemAt(pos)
        if not item:
            return
        shot_id = item.data(Qt.UserRole)
        menu = QMenu(self)
        del_act = menu.addAction("샷 삭제")
        repl_img_act = menu.addAction("이미지 교체")
        act = menu.exec(self._shots_list.mapToGlobal(pos))
        if act == del_act and self._repo:
            self._repo.delete_shot(shot_id)
            self._refresh_shots()
        elif act == repl_img_act:
            self._replace_shot_image(shot_id)

    def _on_rows_moved(self, parent, start, end, dest, row) -> None:  # type: ignore[override]
        # Persist new order
        if not self._repo or self._current_scene_id is None:
            return
        order: list[int] = []
        for i in range(self._shots_list.count()):
            order.append(int(self._shots_list.item(i).data(Qt.UserRole)))
        self._repo.update_images_order(self._current_scene_id, order)

    def _on_import_image(self) -> None:
        from PySide6.QtWidgets import QFileDialog

        db_path = get_current_project_path()
        if not db_path or not self._asset_service:
            self._status.setText("프로젝트가 열려 있지 않거나 초기화되지 않았습니다.")
            return
        # 현재 장면이 없으면 기본 장면 보장
        self._ensure_default_scene()
        if not self._repo:
            self._status.setText("데이터 저장소 초기화 실패")
            return
        scenes = self._repo.list_scenes()
        if not scenes:
            self._status.setText("장면 생성 실패")
            return
        self._current_scene_id = scenes[0].id

        path, _ = QFileDialog.getOpenFileName(self, "이미지 선택", "", "Images (*.png *.jpg *.jpeg *.webp *.bmp);;All Files (*)")
        if not path:
            return
        try:
            asset_id, proj_rel, thumb_rel = self._asset_service.import_image(path)
            if self._current_scene_id is not None:
                new_id = self._repo.create_image(scene_id=self._current_scene_id, description="", asset_id=asset_id)
                self._refresh_shots()
                # select last item
                if self._shots_list.count() > 0:
                    self._shots_list.setCurrentRow(self._shots_list.count() - 1)
            self._status.setText("이미지 임포트 및 저장 완료")
        except Exception as e:
            self._status.setText(f"임포트 실패: {e}")

    def _replace_shot_image(self, shot_id: int) -> None:
        if not self._asset_service or not self._repo:
            return
        path, _ = QFileDialog.getOpenFileName(self, "이미지 선택", "", "Images (*.png *.jpg *.jpeg *.webp *.bmp);;All Files (*)")
        if not path:
            return
        asset_id, proj_rel, thumb_rel = self._asset_service.import_image(path)
        self._repo.link_shot_asset(shot_id, asset_id)
        self._refresh_shots()


