#!/usr/bin/env python3
"""
로컬 빌드 테스트 스크립트
"""

import os
import sys
import subprocess
from pathlib import Path

def test_dependencies():
    """필요한 의존성이 설치되어 있는지 확인합니다."""
    print("의존성 확인 중...")
    
    required_packages = [
        'PySide6',
        'Pillow', 
        'pyinstaller'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.lower().replace('-', '_'))
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} (설치 필요)")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n설치가 필요한 패키지: {', '.join(missing_packages)}")
        print("다음 명령어로 설치하세요:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    print("모든 의존성이 설치되어 있습니다!")
    return True

def test_project_structure():
    """프로젝트 구조가 올바른지 확인합니다."""
    print("\n프로젝트 구조 확인 중...")
    
    required_files = [
        'main.py',
        'requirements.txt',
        'src/cinescribe/app.py',
        'AI_assets',
        '시나리오_assets'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} (누락)")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n누락된 파일/폴더: {', '.join(missing_files)}")
        return False
    
    print("프로젝트 구조가 올바릅니다!")
    return True

def test_pyinstaller():
    """PyInstaller가 제대로 작동하는지 확인합니다."""
    print("\nPyInstaller 테스트 중...")
    
    try:
        result = subprocess.run(
            ['pyinstaller', '--version'], 
            capture_output=True, 
            text=True, 
            check=True
        )
        version = result.stdout.strip()
        print(f"✓ PyInstaller {version}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ PyInstaller 실행 오류: {e}")
        return False
    except FileNotFoundError:
        print("✗ PyInstaller를 찾을 수 없습니다.")
        return False

def test_build_script():
    """빌드 스크립트가 존재하는지 확인합니다."""
    print("\n빌드 스크립트 확인 중...")
    
    build_files = [
        'build_exe.py',
        'CineScriber.spec',
        'build_exe.bat'
    ]
    
    missing_files = []
    
    for file_path in build_files:
        if Path(file_path).exists():
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} (누락)")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n누락된 빌드 파일: {', '.join(missing_files)}")
        return False
    
    print("모든 빌드 파일이 준비되어 있습니다!")
    return True

def main():
    """메인 테스트 함수"""
    print("=" * 50)
    print("CineScriber 빌드 환경 테스트")
    print("=" * 50)
    
    tests = [
        ("의존성 확인", test_dependencies),
        ("프로젝트 구조 확인", test_project_structure),
        ("PyInstaller 확인", test_pyinstaller),
        ("빌드 스크립트 확인", test_build_script)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n[{test_name}]")
        if test_func():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"테스트 결과: {passed}/{total} 통과")
    
    if passed == total:
        print("🎉 모든 테스트가 통과했습니다!")
        print("\n이제 다음 중 하나를 실행할 수 있습니다:")
        print("1. Windows: build_exe.bat")
        print("2. Python: python build_exe.py")
        print("3. GitHub Actions: 태그 푸시 또는 수동 실행")
    else:
        print("❌ 일부 테스트가 실패했습니다.")
        print("위의 오류를 수정한 후 다시 테스트해주세요.")
    
    print("=" * 50)

if __name__ == "__main__":
    main()
