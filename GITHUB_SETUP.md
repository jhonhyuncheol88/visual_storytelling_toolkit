# GitHub 저장소 설정 및 GitHub Actions 사용 가이드

## 🚀 1단계: GitHub 저장소 생성

1. GitHub에 로그인
2. 새 저장소 생성 (New repository)
3. 저장소 이름: `cinescribe` 또는 원하는 이름
4. Public 또는 Private 선택
5. README 파일 생성 체크 해제 (이미 있음)
6. 저장소 생성

## 📥 2단계: 로컬 저장소 설정

```bash
# 현재 디렉토리에서 Git 초기화
git init

# 원격 저장소 추가
git remote add origin https://github.com/사용자명/저장소명.git

# 모든 파일 추가
git add .

# 첫 번째 커밋
git commit -m "초기 커밋: CineScriber 프로젝트"

# 메인 브랜치로 푸시
git branch -M main
git push -u origin main
```

## 🏷️ 3단계: 태그 생성 및 GitHub Actions 실행

### 자동 빌드 트리거 (태그 기반)

```bash
# 버전 태그 생성
git tag v1.0.0

# 태그 푸시 (GitHub Actions 자동 실행)
git push origin v1.0.0
```

### 수동 빌드 실행

1. GitHub 저장소 페이지에서 **Actions** 탭 클릭
2. **Windows Exe 빌드 및 배포** 워크플로우 선택
3. **Run workflow** 버튼 클릭
4. **Run workflow** 클릭하여 실행

## 📦 4단계: 빌드 결과 확인

### GitHub Actions에서 확인

1. **Actions** 탭에서 워크플로우 실행 상태 확인
2. 실행 완료 후 **build-windows** 작업 클릭
3. **빌드 결과 확인** 단계에서 로그 확인

### 결과물 다운로드

#### 자동 배포 (태그 기반)
- **Releases** 탭에서 `v1.0.0` 릴리스 확인
- `CineScriber.exe` 파일 다운로드

#### 수동 실행
- **Actions** → **build-windows** → **CineScriber-Windows** 아티팩트
- `CineScriber.exe` 파일 다운로드

## 🔧 5단계: 문제 해결

### GitHub Actions 오류

1. **권한 문제**
   - 저장소 **Settings** → **Actions** → **General**
   - **Workflow permissions** → **Read and write permissions** 선택

2. **의존성 설치 실패**
   - `requirements.txt` 파일 확인
   - Python 버전 호환성 확인

3. **빌드 실패**
   - Actions 로그에서 구체적인 오류 메시지 확인
   - 로컬에서 `python build_exe.py` 실행하여 테스트

### 로컬 빌드 테스트

```bash
# Windows에서
build_exe.bat

# 또는 Python으로
python build_exe.py
```

## 📋 6단계: 지속적 배포 설정

### 자동화된 릴리스

1. **새 기능 개발** → `main` 브랜치에 푸시
2. **릴리스 준비** → `v1.1.0` 태그 생성
3. **자동 빌드** → GitHub Actions 실행
4. **자동 배포** → GitHub Releases에 업로드

### 브랜치 전략

```
main (안정 버전)
├── develop (개발 버전)
├── feature/새기능 (기능 개발)
└── hotfix/버그수정 (긴급 수정)
```

## 🎯 7단계: 사용자에게 배포

### GitHub Releases 활용

1. **릴리스 노트 작성**
   - 새로운 기능 설명
   - 버그 수정 내용
   - 사용법 가이드

2. **다운로드 링크 공유**
   - GitHub Releases URL 공유
   - 직접 다운로드 링크 제공

### 배포 채널

- **GitHub Releases**: 공식 배포
- **GitHub Actions Artifacts**: 개발자용
- **로컬 빌드**: 테스트용

## 📊 8단계: 모니터링 및 유지보수

### GitHub Actions 모니터링

- 워크플로우 실행 성공률 확인
- 빌드 시간 최적화
- 오류 로그 분석

### 사용자 피드백

- Issues 탭에서 버그 리포트 수집
- Discussions에서 기능 제안 수집
- Pull Requests로 기여 받기

---

**💡 팁**: 첫 번째 빌드는 시간이 오래 걸릴 수 있습니다. PyInstaller가 모든 의존성을 다운로드하고 패키징하기 때문입니다.
