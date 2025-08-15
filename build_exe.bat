@echo off
echo CineScriber Windows Exe 빌드 시작...
echo.

REM Python이 설치되어 있는지 확인
python --version >nul 2>&1
if errorlevel 1 (
    echo 오류: Python이 설치되어 있지 않습니다.
    echo Python을 설치한 후 다시 시도해주세요.
    pause
    exit /b 1
)

REM 가상환경 활성화 (있는 경우)
if exist "venv\Scripts\activate.bat" (
    echo 가상환경을 활성화합니다...
    call venv\Scripts\activate.bat
)

REM 의존성 설치
echo 의존성을 설치합니다...
pip install -r requirements.txt

REM exe 빌드
echo exe 파일을 빌드합니다...
python build_exe.py

if errorlevel 1 (
    echo.
    echo 빌드에 실패했습니다.
    pause
    exit /b 1
)

echo.
echo 빌드가 완료되었습니다!
echo exe 파일은 dist 폴더에 있습니다.
echo.
pause
