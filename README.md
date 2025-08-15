# ShotCanvas - AI 기반 시나리오 작성 도구

ShotCanvas는 AI를 활용한 시나리오 작성, 스토리보드 제작, 시네마틱 시퀀스 관리를 위한 데스크톱 애플리케이션입니다.

## 🚀 다운로드 및 설치

### Windows 사용자

#### 방법 1: GitHub Releases (권장)
1. [Releases 페이지](https://github.com/사용자명/저장소명/releases) 방문
2. 최신 버전의 `ShotCanvas.exe` 다운로드
3. 파일을 원하는 폴더에 저장

#### 방법 2: GitHub Actions Artifacts
1. [Actions 페이지](https://github.com/사용자명/저장소명/actions) 방문
2. 최신 `ShotCanvas-Windows` 아티팩트 다운로드

### 설치 후 실행

1. **Windows 보안 경고 해결**:
   - exe 파일을 우클릭 → "속성"
   - "보안" 섹션에서 "차단 해제" 체크박스 선택
   - "확인" 클릭

2. **Windows Defender 허용**:
   - Windows Defender 알림에서 "추가 정보" 클릭
   - "실행" 버튼 클릭

3. **SmartScreen 우회** (필요시):
   - SmartScreen 경고에서 "추가 정보" 클릭
   - "실행" 버튼 클릭

## 🎯 주요 기능

- **프로젝트 관리**: 시나리오 프로젝트 생성 및 관리
- **AI 비주얼 프롬프트**: AI를 활용한 시각적 아이디어 생성
- **시네마틱 시퀀스**: 영화적 장면 구성 및 관리
- **스토리보드**: 시각적 스토리텔링 도구
- **에셋 관리**: 이미지, 오디오 등 미디어 파일 관리
- **캐릭터 관리**: 등장인물 정보 및 설정 관리

## 🛠️ 개발자용 정보

### 로컬 개발 환경 설정

```bash
# 저장소 클론
git clone https://github.com/사용자명/저장소명.git
cd 저장소명

# 가상환경 생성 및 활성화
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# 의존성 설치
pip install -r requirements.txt

# 개발 모드 실행
python main.py
```

### Windows exe 빌드

```bash
# 배치 파일 사용 (권장)
build_exe.bat

# 또는 Python 스크립트 사용
python build_exe.py

# 또는 spec 파일 직접 사용
pyinstaller build_exe.spec
```

### GitHub Actions를 통한 자동 빌드

1. **태그 기반 자동 빌드**:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. **수동 빌드**: GitHub 저장소의 Actions 탭에서 "Run workflow" 실행

## 📋 시스템 요구사항

- **운영체제**: Windows 10/11 (64비트)
- **메모리**: 최소 4GB RAM (권장 8GB+)
- **저장공간**: 최소 500MB
- **Python**: 3.11+ (개발용)

## 🔧 문제 해결

### 일반적인 문제들

1. **"cinescribe 모듈을 찾을 수 없습니다" 오류**
   - `build_exe.spec` 파일을 사용하여 빌드
   - `--collect-all=cinescribe` 옵션 확인

2. **Windows에서 실행 차단**
   - 파일 속성에서 "차단 해제" 체크
   - Windows Defender에서 "허용" 선택

3. **PySide6 관련 오류**
   - `requirements.txt`에서 PySide6 버전 확인
   - 가상환경 재생성 및 의존성 재설치

### 추가 지원

- **Issues**: [GitHub Issues](https://github.com/사용자명/저장소명/issues)에서 버그 리포트
- **Discussions**: [GitHub Discussions](https://github.com/사용자명/저장소명/discussions)에서 질문 및 제안

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

**💡 팁**: 첫 실행 시 Windows 보안 경고가 나타날 수 있습니다. 이는 정상적인 현상이며, 위의 설치 가이드를 따라 해결할 수 있습니다.
