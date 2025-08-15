#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ShotCanvas - AI 영상 제작 도구
macOS/Windows 응용프로그램으로 패키징하기 위한 진입점
"""

import sys
import os
import platform

def setup_paths_for_os():
    """OS별 경로 설정"""
    print(f"🖥️ OS 감지: {platform.system()} {platform.release()}")
    
    # PyInstaller 환경인지 확인
    if getattr(sys, 'frozen', False):
        print("📦 PyInstaller 환경에서 실행 중")
        # PyInstaller 환경에서는 실행 파일 위치 기준
        base_dir = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
        print(f"✅ PyInstaller base_dir: {base_dir}")
        
        # PyInstaller 환경에서는 이미 모든 모듈이 포함되어 있음
        # 추가 경로 설정 불필요
        return True
    else:
        print("🔧 개발 환경에서 실행 중")
        # 개발 환경에서는 현재 스크립트 위치 기준
        current_dir = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, current_dir)
        print(f"✅ 현재 디렉토리 추가: {current_dir}")
        
        # src 폴더를 Python 경로에 추가
        src_dir = os.path.join(current_dir, "src")
        if os.path.exists(src_dir):
            sys.path.insert(0, src_dir)
            print(f"✅ src 폴더 추가: {src_dir}")
        else:
            print(f"❌ src 폴더를 찾을 수 없음: {src_dir}")
            return False
        
        # cinescribe 폴더를 Python 경로에 추가
        cinescribe_dir = os.path.join(src_dir, "cinescribe")
        if os.path.exists(cinescribe_dir):
            sys.path.insert(0, cinescribe_dir)
            print(f"✅ cinescribe 폴더 추가: {cinescribe_dir}")
        else:
            print(f"❌ cinescribe 폴더를 찾을 수 없음: {cinescribe_dir}")
            return False
        
        # OS별 추가 경로 설정
        if platform.system() == "Darwin":  # macOS
            print("🍎 macOS 환경 감지 - 추가 경로 설정")
            # macOS에서 필요한 추가 경로들
            macos_paths = [
                os.path.join(current_dir, "new_venv", "lib", "python3.13", "site-packages"),
                os.path.join(current_dir, "venv", "lib", "python3.13", "site-packages"),
                os.path.join(current_dir, "venv", "lib", "python3.12", "site-packages"),
                os.path.join(current_dir, "venv", "lib", "python3.11", "site-packages"),
            ]
            for path in macos_paths:
                if os.path.exists(path):
                    sys.path.insert(0, path)
                    print(f"✅ macOS 경로 추가: {path}")
                    break
        
        elif platform.system() == "Windows":  # Windows
            print("🪟 Windows 환경 감지 - 추가 경로 설정")
            # Windows에서 필요한 추가 경로들
            windows_paths = [
                os.path.join(current_dir, "venv", "Lib", "site-packages"),
                os.path.join(current_dir, "env", "Lib", "site-packages"),
                os.path.join(current_dir, "Scripts"),
            ]
            for path in windows_paths:
                if os.path.exists(path):
                    sys.path.insert(0, path)
                    print(f"✅ Windows 경로 추가: {path}")
                    break
        
        else:  # Linux 또는 기타
            print(f"🐧 {platform.system()} 환경 감지")
    
    return True

def run_shotcanvas():
    """ShotCanvas 실행"""
    try:
        print("🚀 ShotCanvas 실행 중...")
        
        # PySide6 import 시도
        try:
            from PySide6.QtWidgets import QApplication
            print("✅ PySide6.QtWidgets import 성공")
        except ImportError as e:
            print(f"❌ PySide6.QtWidgets import 실패: {e}")
            print("PySide6가 설치되어 있는지 확인하세요.")
            return False
        
        # MainWindow import 시도
        try:
            from cinescribe.views.main_window import MainWindow
            print("✅ MainWindow import 성공")
        except ImportError as e:
            print(f"❌ MainWindow import 실패: {e}")
            print("현재 sys.path:")
            for i, path in enumerate(sys.path):
                print(f"  {i}: {path}")
            return False
        
        # GUI 실행
        print("🎬 ShotCanvas GUI 시작...")
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        print("✅ ShotCanvas GUI 실행 성공!")
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"💥 ShotCanvas 실행 실패: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """메인 함수"""
    print("🎬 ShotCanvas - AI 영상 제작 도구")
    print("=" * 60)
    
    try:
        # 1. OS별 경로 설정
        if not setup_paths_for_os():
            print("❌ 경로 설정에 실패했습니다.")
            return
        
        # 2. 현재 Python 경로 표시
        print(f"\n📁 현재 Python 경로 (처음 10개):")
        for i, path in enumerate(sys.path[:10]):
            print(f"  {i:2d}: {path}")
        if len(sys.path) > 10:
            print(f"  ... 및 {len(sys.path) - 10}개 더")
        
        # 3. ShotCanvas 실행
        print("\n" + "=" * 60)
        if not run_shotcanvas():
            print("❌ ShotCanvas 실행에 실패했습니다.")
            return
        
    except Exception as e:
        print(f"\n💥 치명적 오류 발생:")
        print(f"오류: {e}")
        import traceback
        traceback.print_exc()
        
        print("\n프로그램을 종료하려면 아무 키나 누르세요...")
        try:
            input()
        except:
            pass
        
        sys.exit(1)

if __name__ == "__main__":
    main()


