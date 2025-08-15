from __future__ import annotations

import os
import sys


def _ensure_src_on_path() -> None:
    """개발 환경에서 src 폴더를 Python 경로에 추가"""
    here = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.join(here, "src")
    if src_path not in sys.path:
        sys.path.insert(0, src_path)


def _ensure_paths_for_frozen() -> None:
    """PyInstaller로 빌드된 실행 파일(frozen) 환경에서 cinescribe 모듈 경로 보장"""
    if getattr(sys, "frozen", False):
        base_dir = getattr(sys, "_MEIPASS", None) or os.path.dirname(sys.executable)
        
        # PyInstaller가 수집한 모듈들을 찾기 위한 경로들
        candidates = [
            base_dir,  # _MEIPASS 디렉토리 (PyInstaller가 모듈을 여기에 복사)
            os.path.join(base_dir, "src"),
            os.path.join(base_dir, "cinescribe"),
            os.path.join(os.path.dirname(sys.executable), "src"),
        ]
        
        for p in candidates:
            try:
                if os.path.isdir(p) and p not in sys.path:
                    sys.path.insert(0, p)
                    print(f"PyInstaller 경로 추가: {p}")
            except Exception as e:
                print(f"경로 추가 실패 {p}: {e}")


def _try_import_cinescribe() -> bool:
    """cinescribe 모듈 임포트 시도"""
    try:
        import cinescribe.app
        print("cinescribe 모듈 임포트 성공")
        return True
    except ImportError as e:
        print(f"cinescribe 모듈 임포트 실패: {e}")
        return False


def main() -> None:
    """메인 함수 - 개발/배포 환경 모두에서 cinescribe를 찾도록 경로 보장 후 임포트"""
    print("=== ShotCanvas 실행 시작 ===")
    
    # 1단계: 기본 경로 설정
    _ensure_src_on_path()
    _ensure_paths_for_frozen()
    
    # 2단계: cinescribe 모듈 임포트 시도
    if not _try_import_cinescribe():
        # 3단계: 추가 폴백 - 경로 재설정 후 재시도
        print("추가 경로 설정 시도...")
        _ensure_src_on_path()
        _ensure_paths_for_frozen()
        
        if not _try_import_cinescribe():
            print("=== 오류: cinescribe 모듈을 찾을 수 없습니다 ===")
            print("현재 sys.path:")
            for i, path in enumerate(sys.path):
                print(f"  {i}: {path}")
            print("\n현재 작업 디렉토리:", os.getcwd())
            print("실행 파일 위치:", os.path.abspath(__file__))
            sys.exit(1)
    
    # 4단계: 앱 실행
    try:
        from cinescribe.app import main as app_main
        print("앱 메인 함수 호출...")
        app_main()
    except Exception as e:
        print(f"앱 실행 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()


