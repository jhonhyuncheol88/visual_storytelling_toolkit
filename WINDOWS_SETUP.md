# Windows 실행 문제 해결 가이드

## 🔴 주요 문제들

### 1. ModuleNotFoundError: No module named 'cinescribe'
**원인**: PyInstaller가 cinescribe 모듈을 제대로 수집하지 못함
**해결**: 
- `build_exe.spec` 파일을 사용하여 빌드
- `--collect-all=cinescribe` 옵션으로 전체 패키지 수집

### 2. Windows에서 exe 실행 차단
**원인**: 
- 디지털 서명 부재
- Windows Defender/SmartScreen 보안 경고
- 알려지지 않은 출처로 인식

## 🛠️ 해결 방법

### 방법 1: 속성에서 차단 해제
1. exe 파일을 우클릭 → "속성"
2. "보안" 섹션에서 "차단 해제" 체크박스 선택
3. "확인" 클릭

### 방법 2: Windows Defender 허용
1. Windows Defender 알림에서 "추가 정보" 클릭
2. "실행" 버튼 클릭
3. "예" 선택하여 실행 허용

### 방법 3: SmartScreen 우회
1. SmartScreen 경고에서 "추가 정보" 클릭
2. "실행" 버튼 클릭
3. "예" 선택

### 방법 4: 관리자 권한으로 실행
1. exe 파일을 우클릭
2. "관리자 권한으로 실행" 선택

### 방법 5: PowerShell에서 실행 정책 변경
```powershell
# 관리자 권한으로 PowerShell 실행
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 📋 빌드 명령어

### spec 파일 사용 (권장)
```bash
pyinstaller build_exe.spec
```

### 직접 명령어 사용
```bash
pyinstaller --onefile --windowed --name=ShotCanvas --paths=src --collect-all=cinescribe --hidden-import=cinescribe main.py
```

## 🔍 문제 진단

### 로그 확인
빌드 후 `dist` 폴더의 exe 파일을 실행할 때 콘솔 창이 나타나면 오류 메시지를 확인할 수 있습니다.

### 모듈 경로 확인
`main.py`에서 추가된 디버그 출력으로 모듈 경로 문제를 파악할 수 있습니다.

## ⚠️ 주의사항

1. **보안**: 신뢰할 수 있는 소스에서만 exe 파일을 실행하세요
2. **백업**: 중요한 데이터가 있다면 백업 후 테스트하세요
3. **테스트**: 개발 환경에서 충분히 테스트한 후 배포하세요

## 📞 추가 지원

문제가 지속되면:
1. 빌드 로그 확인
2. Python 환경 확인 (가상환경 사용 권장)
3. 의존성 패키지 버전 확인
