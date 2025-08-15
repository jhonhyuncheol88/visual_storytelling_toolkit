#!/usr/bin/env python3
"""
Windows용 exe 파일 빌드 스크립트
"""

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
    
    # PyInstaller 명령어 구성
    cmd = [
        "pyinstaller",
        "--onefile",  # 단일 exe 파일로 생성
        "--windowed",  # 콘솔 창 숨김
        "--name=CineScriber",  # exe 파일 이름
        "--icon=AI_assets/icon.ico" if (current_dir / "AI_assets" / "icon.ico").exists() else "",
        "--add-data=AI_assets;AI_assets",  # AI_assets 폴더 포함
        "--add-data=시나리오_assets;시나리오_assets",  # 시나리오_assets 폴더 포함
        "--hidden-import=PySide6.QtCore",
        "--hidden-import=PySide6.QtGui", 
        "--hidden-import=PySide6.QtWidgets",
        "--hidden-import=PIL",
        "--hidden-import=PIL._tkinter_finder",
        "main.py"
    ]
    
    # 빈 문자열 제거
    cmd = [arg for arg in cmd if arg]
    
    print("빌드 명령어:", " ".join(cmd))
    print("빌드를 시작합니다...")
    
    try:
        # PyInstaller 실행
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("빌드가 성공적으로 완료되었습니다!")
        print(f"exe 파일 위치: {dist_dir / 'CineScriber.exe'}")
        
        # 빌드 결과 확인
        exe_path = dist_dir / "CineScriber.exe"
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"파일 크기: {size_mb:.1f} MB")
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
