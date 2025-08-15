from __future__ import annotations

import os
import sys
import traceback

def main() -> None:
    """Windows 실행 테스트를 위한 최소한의 메인 함수"""
    try:
        print("=== ShotCanvas Windows 실행 테스트 시작 ===")
        print(f"Python 버전: {sys.version}")
        print(f"플랫폼: {sys.platform}")
        print(f"실행 파일: {sys.executable}")
        print(f"현재 작업 디렉토리: {os.getcwd()}")
        print(f"현재 sys.path:")
        for i, path in enumerate(sys.path):
            print(f"  {i}: {path}")
        
        # Windows에서 실행 중인지 확인
        if sys.platform.startswith('win'):
            print("\n=== Windows 환경 감지됨 ===")
            print("Windows에서 실행 중입니다.")
        else:
            print("\n=== 다른 플랫폼에서 실행 중 ===")
        
        # PyInstaller 환경 확인
        if getattr(sys, "frozen", False):
            print("\n=== PyInstaller 환경 감지됨 ===")
            base_dir = getattr(sys, "_MEIPASS", None) or os.path.dirname(sys.executable)
            print(f"PyInstaller base_dir: {base_dir}")
            
            # _MEIPASS 내용 확인
            if os.path.exists(base_dir):
                print(f"base_dir 존재: {base_dir}")
                try:
                    files = os.listdir(base_dir)
                    print(f"base_dir 내용 (처음 10개): {files[:10]}")
                except Exception as e:
                    print(f"base_dir 내용 읽기 실패: {e}")
            else:
                print(f"base_dir 존재하지 않음: {base_dir}")
        else:
            print("\n=== 개발 환경에서 실행 중 ===")
        
        # cinescribe 모듈 임포트 시도
        print("\n=== cinescribe 모듈 임포트 시도 ===")
        try:
            import cinescribe
            print("✅ cinescribe 모듈 임포트 성공!")
            print(f"cinescribe 위치: {cinescribe.__file__}")
        except ImportError as e:
            print(f"❌ cinescribe 모듈 임포트 실패: {e}")
            print("현재 sys.path에서 cinescribe 검색...")
            
            # sys.path에서 cinescribe 검색
            for path in sys.path:
                if os.path.exists(path):
                    try:
                        files = os.listdir(path)
                        if 'cinescribe' in files:
                            print(f"✅ cinescribe 발견: {path}")
                            break
                    except Exception:
                        continue
            else:
                print("❌ sys.path에서 cinescribe를 찾을 수 없음")
        
        # PySide6 임포트 시도
        print("\n=== PySide6 모듈 임포트 시도 ===")
        try:
            import PySide6
            print("✅ PySide6 모듈 임포트 성공!")
            print(f"PySide6 위치: {PySide6.__file__}")
        except ImportError as e:
            print(f"❌ PySide6 모듈 임포트 실패: {e}")
        
        print("\n=== 테스트 완료 ===")
        print("아무 키나 누르면 종료됩니다...")
        
        # Windows에서 사용자 입력 대기
        if sys.platform.startswith('win'):
            try:
                input()
            except:
                pass
        
    except Exception as e:
        print(f"\n=== 치명적 오류 발생 ===")
        print(f"오류: {e}")
        print("상세 오류 정보:")
        traceback.print_exc()
        
        # Windows에서 사용자 입력 대기
        if sys.platform.startswith('win'):
            print("\n아무 키나 누르면 종료됩니다...")
            try:
                input()
            except:
                pass
        
        sys.exit(1)

if __name__ == "__main__":
    main()


