# 기여 가이드

SBOM Tools 프로젝트에 기여해 주셔서 감사합니다! 이 문서는 프로젝트에 기여하는 방법을 안내합니다.

## 목차

- [행동 강령](#행동-강령)
- [기여 방법](#기여-방법)
- [개발 환경 설정](#개발-환경-설정)
- [코드 스타일](#코드-스타일)
- [커밋 메시지 규칙](#커밋-메시지-규칙)
- [Pull Request 절차](#pull-request-절차)
- [이슈 보고](#이슈-보고)
- [문의](#문의)

## 행동 강령

이 프로젝트는 모든 기여자가 존중받고 환영받는 환경을 만들기 위해 노력합니다. 프로젝트 참여자는 다음을 준수해야 합니다:

- **존중**: 다른 사람의 의견과 경험을 존중합니다
- **협력**: 건설적인 피드백을 제공하고 받아들입니다
- **포용**: 다양한 배경과 관점을 환영합니다
- **전문성**: 전문적이고 친절한 태도를 유지합니다

부적절한 행동을 목격하거나 경험한 경우 opensource@sktelecom.com으로 연락해주세요.

## 기여 방법

다음과 같은 방법으로 프로젝트에 기여할 수 있습니다:

### 1. 버그 리포트

버그를 발견하셨나요? [이슈](https://github.com/sktelecom/sbom-tools/issues/new?template=bug_report.md)를 작성해주세요.

**포함해야 할 정보**:
- 명확한 제목
- 재현 단계
- 예상 동작과 실제 동작
- 환경 정보 (OS, Docker 버전 등)
- 로그나 스크린샷

### 2. 기능 제안

새로운 기능을 제안하고 싶으신가요? [기능 요청](https://github.com/sktelecom/sbom-tools/issues/new?template=feature_request.md)을 작성해주세요.

**포함해야 할 정보**:
- 제안하는 기능의 설명
- 사용 사례 및 필요성
- 가능하면 구현 방법 제안

### 3. 코드 기여

코드를 직접 기여하고 싶으신가요? Pull Request를 환영합니다!

**기여할 수 있는 영역**:
- 버그 수정
- 새로운 기능 추가
- 성능 개선
- 문서 개선
- 테스트 추가
- 새로운 패키지 매니저 지원 추가

**개발 가이드**:
- [ARCHITECTURE.md](ARCHITECTURE.md) - 시스템 아키텍처 이해
- [PACKAGE_MANAGER_GUIDE.md](PACKAGE_MANAGER_GUIDE.md) - 패키지 매니저 추가 방법
- [TESTING_GUIDE.md](TESTING_GUIDE.md) - 테스트 작성 및 실행
- 다국어 지원 (영문 번역 등)

### 4. 문서 개선

문서에 오류가 있거나 개선이 필요한 부분이 있나요?
- README 개선
- 가이드 문서 추가 또는 수정
- 예제 프로젝트 추가
- 주석 개선

## 개발 환경 설정

### 1. 저장소 Fork 및 Clone

```bash
# 저장소 Fork
# GitHub에서 'Fork' 버튼 클릭

# Clone
git clone https://github.com/YOUR_USERNAME/sbom-tools.git
cd sbom-tools

# 원본 저장소를 upstream으로 추가
git remote add upstream https://github.com/sktelecom/sbom-tools.git
```

### 2. 필수 도구 설치

- **Docker**: 20.10 이상
- **jq**: JSON 처리 (테스트용)
- **ShellCheck**: Bash 스크립트 린팅 (선택)

```bash
# Ubuntu/Debian
sudo apt-get install docker.io jq shellcheck

# macOS
brew install docker jq shellcheck
```

### 3. 개발 브랜치 생성

```bash
# 최신 코드 동기화
git checkout main
git pull upstream main

# 새 브랜치 생성
git checkout -b feature/your-feature-name
# 또는
git checkout -b fix/your-bug-fix
```

### 4. 테스트 실행

변경 사항을 테스트하세요:

```bash
# 실행 권한 부여
chmod +x scripts/scan-sbom.sh
chmod +x tests/test-scan.sh

# 통합 테스트 실행
./tests/test-scan.sh
```

## 코드 스타일

### Bash 스크립트

```bash
#!/bin/bash
# Copyright 2026 SK Telecom Co., Ltd.
#
# Licensed under the Apache License, Version 2.0

# 명확한 변수명 사용
PROJECT_NAME="MyApp"
VERSION="1.0.0"

# 함수에 주석 추가
# SBOM 파일 이름 생성
generate_filename() {
    local project=$1
    local version=$2
    echo "${project}_${version}_bom.json"
}

# 에러 처리
if [ ! -f "package.json" ]; then
    echo "[ERROR] package.json not found"
    exit 1
fi
```

**가이드라인**:
- `set -e` 사용으로 에러 시 즉시 종료
- 명확하고 설명적인 변수명
- 함수에는 주석 추가
- 에러 메시지는 `[ERROR]` 접두사 사용
- ShellCheck 경고 해결

### Markdown 문서

```markdown
# 제목은 H1 하나만

## 섹션은 H2부터 시작

### 하위 섹션

- 리스트는 `-` 사용
- 명확하고 간결한 문장
- 코드 블록에는 언어 지정

\`\`\`bash
echo "Hello World"
\`\`\`
```

**가이드라인**:
- 한 줄은 80-120자 이내
- 코드 블록에는 언어 지정
- 링크는 상대 경로 우선
- 이미지는 `docs/images/` 디렉토리에 저장

### Dockerfile

```dockerfile
# 명확한 베이스 이미지 버전 지정
FROM node:18-alpine

# 레이블 추가
LABEL maintainer="SK Telecom OSPO"

# 한 RUN에서 여러 명령 실행 (레이어 최소화)
RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

# .dockerignore 활용
COPY . /app
```

## 커밋 메시지 규칙

우리는 [Conventional Commits](https://www.conventionalcommits.org/) 스타일을 따릅니다.

### 형식

```
<타입>(<범위>): <제목>

<본문>

<푸터>
```

### 타입

- **feat**: 새로운 기능
- **fix**: 버그 수정
- **docs**: 문서만 변경
- **style**: 코드 의미에 영향을 주지 않는 변경 (포맷팅 등)
- **refactor**: 리팩토링
- **test**: 테스트 추가 또는 수정
- **chore**: 빌드 프로세스 또는 도구 변경

### 예시

```bash
# 좋은 예
feat(scripts): Add Windows batch script support
fix(docker): Resolve Python 2 installation issue
docs(README): Update installation instructions
test(examples): Add Java Gradle example project

# 나쁜 예
update script
fix bug
change dockerfile
```

**자세한 예시**:

```
feat(scripts): Add support for pnpm package manager

- Add pnpm-lock.yaml detection
- Update scan logic to handle pnpm projects
- Add pnpm example in documentation

Closes #123
```

## Pull Request 절차

### 1. 변경 사항 커밋

```bash
# 파일 추가
git add .

# 커밋
git commit -m "feat(scripts): Add new feature"
```

### 2. 원격 저장소에 푸시

```bash
git push origin feature/your-feature-name
```

### 3. Pull Request 생성

1. GitHub에서 저장소로 이동
2. "Pull requests" → "New pull request" 클릭
3. 템플릿에 따라 내용 작성
4. "Create pull request" 클릭

### 4. PR 체크리스트

Pull Request를 생성하기 전에 다음을 확인하세요:

- [ ] 코드가 테스트를 통과하는가? (`./tests/test-scan.sh`)
- [ ] 문서가 업데이트되었는가?
- [ ] 커밋 메시지가 규칙을 따르는가?
- [ ] ShellCheck 경고가 없는가?
- [ ] 기존 기능이 정상 동작하는가?

### 5. 코드 리뷰

- 리뷰어의 피드백에 적극적으로 응답하세요
- 요청된 변경 사항을 반영하세요
- 논의가 필요한 경우 명확하게 설명하세요

### 6. 머지

모든 리뷰가 완료되고 CI가 통과하면 메인테이너가 PR을 머지합니다.

## 이슈 보고

### 버그 리포트

버그를 발견하면 [버그 리포트 템플릿](https://github.com/sktelecom/sbom-tools/issues/new?template=bug_report.md)을 사용하세요.

**좋은 버그 리포트**:

```markdown
### 문제 설명
Docker 이미지 스캔 시 permission denied 오류 발생

### 재현 단계
1. `./scan-sbom.sh --target nginx:alpine --project Test --version 1.0 --generate-only` 실행
2. 다음 오류 발생: "permission denied while trying to connect to Docker"

### 예상 동작
Docker 이미지가 정상적으로 스캔되어야 함

### 실제 동작
Permission denied 오류로 실패

### 환경
- OS: Ubuntu 22.04
- Docker: 24.0.7
- 사용자 그룹: docker 그룹에 속하지 않음

### 추가 정보
로그 파일 첨부
```

### 기능 요청

새로운 기능을 제안하려면 [기능 요청 템플릿](https://github.com/sktelecom/sbom-tools/issues/new?template=feature_request.md)을 사용하세요.

## 자주 묻는 질문

### Q: 작은 오타 수정도 PR을 만들어야 하나요?

**A**: 네! 모든 기여를 환영합니다. 작은 오타 수정도 프로젝트 품질 향상에 도움이 됩니다.

### Q: 새로운 언어 지원을 추가하고 싶습니다.

**A**: 훌륭합니다! 먼저 이슈를 생성하여 논의해주세요. 다음을 포함해야 합니다:
- 지원할 언어/패키지 매니저
- 사용 사례
- 구현 계획

### Q: 문서만 번역하는 것도 기여인가요?

**A**: 물론입니다! 영문 번역이나 다른 언어 지원은 큰 도움이 됩니다.

### Q: CI 테스트가 실패했습니다.

**A**: CI 로그를 확인하여 어떤 테스트가 실패했는지 확인하세요. 로컬에서 `./tests/test-scan.sh`를 실행하여 재현할 수 있습니다.

### Q: 리뷰가 언제 진행되나요?

**A**: 보통 2-3 영업일 내에 리뷰가 진행됩니다. 긴급한 버그 수정은 더 빨리 처리됩니다.

## 개발 팁

### 로컬에서 Docker 이미지 빌드

```bash
cd docker
docker build -t sbom-scanner:dev .
```

### 특정 언어 테스트만 실행

테스트 스크립트를 수정하여 특정 부분만 실행할 수 있습니다:

```bash
# tests/test-scan.sh의 특정 테스트만 주석 해제
```

### ShellCheck로 스크립트 검증

```bash
shellcheck scripts/scan-sbom.sh
shellcheck docker/entrypoint.sh
```

### 문서 로컬 프리뷰

Markdown 파일을 로컬에서 미리 보려면:

```bash
# VS Code 사용
code README.md
# Markdown Preview Enhanced 확장 설치

# 또는 GitHub Flavored Markdown 렌더러 사용
npm install -g markdown-it
markdown-it README.md > README.html
```

## 라이선스

기여하신 코드는 [Apache License 2.0](LICENSE)에 따라 라이선스됩니다. Pull Request를 제출함으로써 귀하는 귀하의 기여가 이 라이선스에 따라 라이선스될 수 있음에 동의하는 것입니다.

## 감사 인사

기여해주신 모든 분들께 감사드립니다! 귀하의 시간과 노력이 이 프로젝트를 더 좋게 만듭니다.

### 기여자 목록

GitHub의 [Contributors](https://github.com/sktelecom/sbom-tools/graphs/contributors) 페이지에서 모든 기여자를 확인할 수 있습니다.

## 문의

질문이나 도움이 필요하신가요?

- **이메일**: opensource@sktelecom.com
- **이슈**: [GitHub Issues](https://github.com/sktelecom/sbom-tools/issues)
- **토론**: [GitHub Discussions](https://github.com/sktelecom/sbom-tools/discussions) (있는 경우)

---

**다시 한 번 기여해 주셔서 감사합니다! **
