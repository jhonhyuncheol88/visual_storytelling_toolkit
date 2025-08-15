@echo off
chcp 65001 >nul
echo === ShotCanvas Windows 빌드 시작 ===

REM Python 가상환경 활성화 (있는 경우)
if exist "venv\Scripts\activate.bat" (
    echo 가상환경 활성화 중...
    call venv\Scripts\activate.bat
)

REM 기존 빌드 폴더 정리
if exist "dist" (
    echo 기존 dist 폴더 정리 중...
    rmdir /s /q "dist"
)
if exist "build" (
    echo 기존 build 폴더 정리 중...
    rmdir /s /q "build"
)

REM PyInstaller로 빌드
echo PyInstaller 빌드 시작...
pyinstaller build_exe.spec

if %ERRORLEVEL% EQU 0 (
    echo.
    echo === 빌드 성공! ===
    echo exe 파일 위치: dist\ShotCanvas.exe
    
    REM 파일 크기 확인
    for %%F in (dist\ShotCanvas.exe) do (
        set /a size=%%~zF/1024/1024
        echo 파일 크기: !size! MB
    )
    
    echo.
    echo === Windows 실행 팁 ===
    echo 1. exe 파일을 우클릭 → 속성 → 보안 → "차단 해제" 체크
    echo 2. Windows Defender에서 "허용" 선택
    echo 3. SmartScreen 경고에서 "추가 정보" → "실행" 클릭
    echo 4. 또는 exe 파일을 우클릭 → "관리자 권한으로 실행"
    
    echo.
    echo 빌드 완료! dist 폴더를 확인하세요.
) else (
    echo.
    echo === 빌드 실패 ===
    echo 오류 코드: %ERRORLEVEL%
    echo 로그를 확인하고 문제를 해결하세요.
)

pause
