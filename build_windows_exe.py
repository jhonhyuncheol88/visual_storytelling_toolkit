#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows 전용 .exe 빌드 스크립트
macOS에서 Windows .exe를 빌드하기 위한 최적화된 설정
"""

import os
import sys
import subprocess
import platform

def build_windows_exe():
    """Windows .exe 빌드"""
    print("🪟 Windows .exe 빌드 시작...")
    
    # 현재 OS 확인
    current_os = platform.system()
    print(f"현재 OS: {current_os}")
    
    if current_os == "Windows":
        print("✅ Windows에서 직접 빌드")
        build_command = [
            "pyinstaller",
            "--onefile",  # 단일 파일로 빌드
            "--windowed",  # GUI 모드
            "--name=ShotCanvas",
            "--paths=src",
            "--paths=src/cinescribe",
            "--collect-all=cinescribe",
            "--collect-all=PySide6",
            "--collect-all=PIL",
            "--hidden-import=PySide6.QtWidgets",
            "--hidden-import=PySide6.QtCore",
            "--hidden-import=PySide6.QtGui",
            "--hidden-import=PySide6.QtNetwork",
            "--hidden-import=PySide6.QtOpenGL",
            "--hidden-import=PySide6.QtPrintSupport",
            "--hidden-import=PySide6.QtSql",
            "--hidden-import=PySide6.QtSvg",
            "--hidden-import=PySide6.QtTest",
            "--hidden-import=PySide6.QtXml",
            "--hidden-import=shiboken6",
            "--hidden-import=sqlite3",
            "--hidden-import=platform",
            "--hidden-import=traceback",
            "--add-data=src/cinescribe;cinescribe",
            "--win-private-assemblies",
            "--clean",
            "main.py"
        ]
    else:
        print("🍎 macOS에서 Windows .exe 빌드 시도")
        print("⚠️  Wine이 설치되어 있어야 합니다")
        
        # Wine을 통한 Windows Python 실행
        build_command = [
            "wine", "python", "-m", "PyInstaller",
            "--onefile",
            "--windowed",
            "--name=ShotCanvas",
            "--paths=src",
            "--paths=src/cinescribe",
            "--collect-all=cinescribe",
            "--collect-all=PySide6",
            "--collect-all=PIL",
            "--hidden-import=PySide6.QtWidgets",
            "--hidden-import=PySide6.QtCore",
            "--hidden-import=PySide6.QtGui",
            "--hidden-import=PySide6.QtNetwork",
            "--hidden-import=PySide6.QtOpenGL",
            "--hidden-import=PySide6.QtPrintSupport",
            "--hidden-import=PySide6.QtSql",
            "--hidden-import=PySide6.QtSvg",
            "--hidden-import=PySide6.QtTest",
            "--hidden-import=PySide6.QtXml",
            "--hidden-import=shiboken6",
            "--hidden-import=sqlite3",
            "--hidden-import=platform",
            "--hidden-import=traceback",
            "--add-data=src/cinescribe;cinescribe",
            "--win-private-assemblies",
            "--clean",
            "main.py"
        ]
    
    try:
        print("🚀 빌드 명령 실행 중...")
        print(f"명령: {' '.join(build_command)}")
        
        result = subprocess.run(
            build_command,
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        
        if result.returncode == 0:
            print("✅ Windows .exe 빌드 성공!")
            print("📁 결과 파일:")
            if os.path.exists("dist/ShotCanvas.exe"):
                print("  - dist/ShotCanvas.exe")
            else:
                print("  - dist/ 폴더 확인 필요")
        else:
            print("❌ Windows .exe 빌드 실패!")
            print("오류 출력:")
            print(result.stderr)
            print("표준 출력:")
            print(result.stdout)
            
    except FileNotFoundError as e:
        print(f"❌ 명령을 찾을 수 없음: {e}")
        if current_os != "Windows":
            print("💡 Wine과 Windows Python을 설치해야 합니다")
    except Exception as e:
        print(f"❌ 빌드 중 오류 발생: {e}")

def check_dependencies():
    """의존성 확인"""
    print("🔍 의존성 확인 중...")
    
    # PyInstaller 확인
    try:
        import PyInstaller
        print(f"✅ PyInstaller: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller가 설치되지 않음")
        return False
    
    # PySide6 확인
    try:
        import PySide6
        print(f"✅ PySide6: {PySide6.__version__}")
    except ImportError:
        print("❌ PySide6가 설치되지 않음")
        return False
    
    # Wine 확인 (macOS에서)
    if platform.system() != "Windows":
        try:
            result = subprocess.run(["wine", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Wine: {result.stdout.strip()}")
            else:
                print("❌ Wine이 설치되지 않음")
                return False
        except FileNotFoundError:
            print("❌ Wine이 설치되지 않음")
            return False
    
    return True

def main():
    """메인 함수"""
    print("🎬 ShotCanvas Windows .exe 빌더")
    print("=" * 50)
    
    if not check_dependencies():
        print("❌ 필요한 의존성이 설치되지 않았습니다.")
        return
    
    build_windows_exe()
    
    print("\n" + "=" * 50)
    print("빌드 완료!")

if __name__ == "__main__":
    main()
