# CineScriber - AI 기반 시나리오 작성 도구

CineScriber는 AI를 활용한 시나리오 작성 및 영상 제작 지원 도구입니다.

## 🚀 기능

- AI 기반 시나리오 작성 지원
- 캐릭터 및 장면 관리
- 스토리보드 생성
- 시각적 프롬프트 생성
- 프로젝트 라이브러리 관리

## 📋 요구사항

- Python 3.11 이상
- Windows 10/11 (exe 빌드용)
- PySide6 (Qt GUI 프레임워크)
- Pillow (이미지 처리)

## 🛠️ 설치 및 실행

### 개발 환경에서 실행

```bash
# 저장소 클론
git clone <repository-url>
cd 시나리오_프로그램

# 가상환경 생성 (권장)
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# 의존성 설치
pip install -r requirements.txt

# 애플리케이션 실행
python main.py
```

### Windows Exe 파일로 실행

1. **자동 빌드 (GitHub Actions)**
   - GitHub 저장소에 코드를 푸시
   - 태그를 생성하여 GitHub Actions 실행
   - `dist/CineScriber.exe` 파일 다운로드

2. **로컬 빌드**
   ```bash
   # Windows에서
   build_exe.bat
   
   # 또는 Python으로
   python build_exe.py
   ```

## 🔧 빌드 설정

### PyInstaller 설정

- `CineScriber.spec`: PyInstaller 설정 파일
- `build_exe.py`: 빌드 스크립트
- `build_exe.bat`: Windows 배치 파일

### 포함되는 파일

- `AI_assets/`: AI 관련 에셋
- `시나리오_assets/`: 시나리오 관련 에셋
- 모든 Python 모듈 및 의존성

## 📦 GitHub Actions

자동 빌드 및 배포를 위한 GitHub Actions 워크플로우가 포함되어 있습니다:

- **트리거**: 태그 푸시 또는 수동 실행
- **플랫폼**: Windows
- **결과**: GitHub Releases에 exe 파일 자동 업로드

### 사용 방법

1. 코드를 GitHub에 푸시
2. 태그 생성: `git tag v1.0.0 && git push origin v1.0.0`
3. GitHub Actions에서 자동 빌드 실행
4. Releases에서 exe 파일 다운로드

## 🏗️ 프로젝트 구조

```
시나리오_프로그램/
├── src/cinescribe/          # 메인 애플리케이션
│   ├── views/               # UI 뷰
│   ├── service/             # 비즈니스 로직
│   ├── repository/          # 데이터 접근
│   └── domain/              # 도메인 모델
├── AI_assets/               # AI 관련 에셋
├── 시나리오_assets/          # 시나리오 관련 에셋
├── main.py                  # 진입점
├── build_exe.py             # 빌드 스크립트
├── CineScriber.spec         # PyInstaller 설정
└── .github/workflows/       # GitHub Actions
```

## 🐛 문제 해결

### 빌드 오류

1. **PyInstaller 오류**: `pip install --upgrade pyinstaller`
2. **의존성 누락**: `pip install -r requirements.txt`
3. **경로 문제**: 절대 경로 사용 확인

### 실행 오류

1. **DLL 누락**: Visual C++ 재배포 패키지 설치
2. **권한 문제**: 관리자 권한으로 실행
3. **파일 경로**: 한글 경로 문제 가능성

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 🤝 기여

버그 리포트, 기능 제안, 풀 리퀘스트를 환영합니다!

---

**참고**: 이 도구는 Windows 환경에서 테스트되었습니다.
