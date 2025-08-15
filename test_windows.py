#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows 실행 테스트 코드
ShotCanvas가 Windows에서 실행되지 않는 문제를 진단
"""

import sys
import os
import platform

def test_windows_environment():
    """Windows 환경 테스트"""
    print("🪟 Windows 환경 테스트 시작")
    print("=" * 50)
    
    # 1. 기본 시스템 정보
    print(f"Python 버전: {sys.version}")
    print(f"플랫폼: {platform.system()} {platform.release()}")
    print(f"아키텍처: {platform.architecture()}")
    print(f"실행 파일: {sys.executable}")
    print(f"현재 작업 디렉토리: {os.getcwd()}")
    
    # 2. Python 경로 테스트
    print(f"\n📁 Python 경로:")
    for i, path in enumerate(sys.path[:10]):
        print(f"  {i:2d}: {path}")
    if len(sys.path) > 10:
        print(f"  ... 및 {len(sys.path) - 10}개 더")
    
    # 3. 필수 모듈 테스트
    print(f"\n🧪 필수 모듈 테스트:")
    
    # PySide6 테스트
    try:
        import PySide6
        print(f"✅ PySide6: {PySide6.__file__}")
    except ImportError as e:
        print(f"❌ PySide6: {e}")
    
    # cinescribe 테스트
    try:
        import cinescribe
        print(f"✅ cinescribe: {cinescribe.__file__}")
    except ImportError as e:
        print(f"❌ cinescribe: {e}")
    
    # 4. 파일 존재 테스트
    print(f"\n📂 파일 존재 테스트:")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    files_to_check = [
        "main.py",
        "src/cinescribe/views/main_window.py",
        "src/cinescribe/__init__.py"
    ]
    
    for file_path in files_to_check:
        full_path = os.path.join(current_dir, file_path)
        if os.path.exists(full_path):
            print(f"✅ {file_path}: 존재")
        else:
            print(f"❌ {file_path}: 없음")
    
    # 5. 경로 설정 테스트
    print(f"\n🔧 경로 설정 테스트:")
    
    # src 폴더 추가
    src_dir = os.path.join(current_dir, "src")
    if os.path.exists(src_dir):
        if src_dir not in sys.path:
            sys.path.insert(0, src_dir)
            print(f"✅ src 폴더를 sys.path에 추가: {src_dir}")
        else:
            print(f"ℹ️ src 폴더가 이미 sys.path에 존재: {src_dir}")
    else:
        print(f"❌ src 폴더를 찾을 수 없음: {src_dir}")
    
    # cinescribe 폴더 추가
    cinescribe_dir = os.path.join(src_dir, "cinescribe")
    if os.path.exists(cinescribe_dir):
        if cinescribe_dir not in sys.path:
            sys.path.insert(0, cinescribe_dir)
            print(f"✅ cinescribe 폴더를 sys.path에 추가: {cinescribe_dir}")
        else:
            print(f"ℹ️ cinescribe 폴더가 이미 sys.path에 존재: {cinescribe_dir}")
    else:
        print(f"❌ cinescribe 폴더를 찾을 수 없음: {cinescribe_dir}")
    
    # 6. 최종 import 테스트
    print(f"\n🎯 최종 import 테스트:")
    
    try:
        from cinescribe.views.main_window import MainWindow
        print("✅ MainWindow import 성공!")
        
        # GUI 실행 테스트
        print("🎬 GUI 실행 테스트 시작...")
        from PySide6.QtWidgets import QApplication
        
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        print("✅ GUI 실행 성공! 창이 열렸습니다.")
        
        # 3초 후 자동 종료 (테스트용)
        import time
        time.sleep(3)
        print("테스트 완료 - 프로그램을 종료합니다.")
        
    except Exception as e:
        print(f"❌ 최종 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
    
    print(f"\n" + "=" * 50)
    print("Windows 테스트 완료")
    print("아무 키나 누르면 종료됩니다...")
    
    try:
        input()
    except:
        pass

if __name__ == "__main__":
    test_windows_environment()
