from __future__ import annotations

import os
import sys


def _ensure_src_on_path() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.join(here, "src")
    if src_path not in sys.path:
        sys.path.insert(0, src_path)


def _ensure_paths_for_frozen() -> None:
    # PyInstaller로 빌드된 실행 파일(frozen) 환경에서 cinescribe 모듈 경로 보장
    if getattr(sys, "frozen", False):
        base_dir = getattr(sys, "_MEIPASS", None) or os.path.dirname(sys.executable)
        candidates = [
            os.path.join(base_dir, "src"),
            os.path.join(base_dir, "cinescribe"),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"),
        ]
        for p in candidates:
            try:
                if os.path.isdir(p) and p not in sys.path:
                    sys.path.insert(0, p)
            except Exception:
                pass


# PyInstaller가 정적 분석으로 패키지를 수집할 수 있도록 더미 임포트 시도
try:
    import cinescribe.app as _pyinstaller_collect_hint  # type: ignore
except Exception:
    _pyinstaller_collect_hint = None  # noqa: F401


def main() -> None:
    # 개발 환경/배포 환경 모두에서 cinescribe를 찾도록 경로 보장 후 임포트
    _ensure_src_on_path()
    _ensure_paths_for_frozen()
    try:
        from cinescribe.app import main as app_main
    except ModuleNotFoundError:
        # 추가 폴백: 한 번 더 경로 보장 후 재시도
        _ensure_src_on_path()
        _ensure_paths_for_frozen()
        from cinescribe.app import main as app_main

    app_main()


if __name__ == "__main__":
    main()


