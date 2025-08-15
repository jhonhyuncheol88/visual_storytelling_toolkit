from __future__ import annotations

import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_exe():
    """PyInstaller를 사용하여 exe 파일을 빌드합니다."""
    
    # 현재 디렉토리
    current_dir = Path(__file__).parent
    dist_dir = current_dir / "dist"
    build_dir = current_dir / "build"
    
    # 기존 빌드 폴더 정리
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    if build_dir.exists():
        shutil.rmtree(build_dir)
    
    # PyInstaller 명령어 구성 - cinescribe 모듈 수집 개선
    cmd = [
        "pyinstaller",
        "--onefile",  # 단일 exe 파일로 생성
        "--console",  # Windows에서 콘솔 창 표시 (디버깅용)
        "--name=ShotCanvas",  # exe 파일 이름
        "--paths=src",  # src 폴더를 Python 경로에 추가
        "--collect-all=cinescribe",  # cinescribe 패키지 전체 수집
        "--hidden-import=cinescribe",
        "--hidden-import=cinescribe.app",
        "--hidden-import=cinescribe.domain",
        "--hidden-import=cinescribe.repository",
        "--hidden-import=cinescribe.service",
        "--hidden-import=cinescribe.utils",
        "--hidden-import=cinescribe.viewmodel",
        "--hidden-import=cinescribe.views",
        "--hidden-import=cinescribe.widgets",
        "--hidden-import=PySide6.QtCore",
        "--hidden-import=PySide6.QtGui", 
        "--hidden-import=PySide6.QtWidgets",
        "--hidden-import=PIL",
        "--hidden-import=PIL._tkinter_finder",
        "--clean",  # 이전 빌드 캐시 정리
        "main.py"
    ]
    
    print("빌드 명령어:", " ".join(cmd))
    print("빌드를 시작합니다...")
    
    try:
        # PyInstaller 실행
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("빌드가 성공적으로 완료되었습니다!")
        print(f"exe 파일 위치: {dist_dir / 'ShotCanvas.exe'}")
        
        # 빌드 결과 확인
        exe_path = dist_dir / "ShotCanvas.exe"
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"파일 크기: {size_mb:.1f} MB")
            
            # Windows 호환성을 위한 추가 정보
            print("\n=== Windows 실행 팁 ===")
            print("1. exe 파일을 우클릭 → '속성' → '보안' → '차단 해제' 체크")
            print("2. Windows Defender에서 '허용' 선택")
            print("3. SmartScreen 경고에서 '추가 정보' → '실행' 클릭")
        else:
            print("경고: exe 파일을 찾을 수 없습니다.")
            
    except subprocess.CalledProcessError as e:
        print(f"빌드 실패: {e}")
        print(f"에러 출력: {e.stderr}")
        return False
    except Exception as e:
        print(f"예상치 못한 오류: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = build_exe()
    if not success:
        sys.exit(1)
