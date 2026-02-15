# GitHub 배포 최종 체크리스트

## 배포 전 최종 확인

### 1. 파일 구조 확인

```bash
cd /mnt/user-data/outputs/sbom-tools

# 전체 파일 목록 확인
find . -type f -not -path './.git/*' -not -name '*.bak' | sort
```

### 2. 백업 파일 정리

현재 `.bak` 파일들이 있습니다:
- scripts/scan-sbom.sh.bak
- scripts/scan-sbom.bat.bak
- docker/entrypoint.sh.bak
- docker/Dockerfile.bak
- tests/test-scan.sh.bak
- .github/workflows/*.yml.bak

**결정 필요:**
- [ ] `.bak` 파일 삭제 (권장)
- [ ] `.bak` 파일 유지 (히스토리용)

**권장: 삭제**
```bash
find . -name "*.bak" -type f -delete
```

### 3. 불필요한 문서 파일 정리

다음 문서들은 개발 과정의 메모이며, 사용자에게 불필요할 수 있습니다:
- ENGLISH_CONVERSION_GUIDE.md
- ENGLISH_CONVERSION_COMPLETE.md
- TESTING_PLAN.md
- TROUBLESHOOTING_TEST.md
- FIX_TEST10.md
- WORKFLOW_STRATEGY.md
- DOCKER_TAG_STRATEGY.md
- DOCKER_BUILD_OPTIMIZATION.md
- DOCKER_DEPLOYMENT_STRATEGY.md
- DOCKER_IMAGE_TAG_STRATEGY.md
- DOCKER_SIZE_OPTIMIZATION.md
- DOCKERFILE_OPTIMIZATION_COMPLETE.md
- SCRIPT_UPDATES_SUMMARY.md
- DOCUMENTATION_UPDATES.md
- README_UPDATES_SUMMARY.md
- COMPLETE_DOCS_UPDATE.md
- TRANSLATION_PLAN.md
- MULTILINGUAL_STRATEGY.md
- PHASE*.md 파일들

**결정 필요:**
- [ ] 모두 삭제 (깔끔한 저장소)
- [ ] `docs/development/` 폴더로 이동 (히스토리 보존)
- [ ] 일부만 유지 (CONTRIBUTING.md는 유지 필수)

**권장: 개발 문서 폴더로 이동**
```bash
mkdir -p docs/development
mv *_PLAN.md *_STRATEGY.md *_COMPLETE.md *_SUMMARY.md PHASE*.md docs/development/ 2>/dev/null
```

### 4. 필수 유지 파일

다음 파일들은 반드시 루트에 유지:
- ✅ README.md (영문)
- ✅ README.ko.md (한글)
- ✅ CONTRIBUTING.md (기여 가이드)
- ✅ LICENSE (라이선스)
- ✅ .gitignore

### 5. Git 설정 확인

**.gitignore 확인:**
```bash
cat .gitignore
```

필요한 내용:
```
# SBOM outputs
*_bom.json

# Test workspace
tests/test-workspace/

# OS files
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
*.swp

# Logs
*.log

# Dependencies
node_modules/
venv/
__pycache__/

# Build outputs
dist/
build/
*.egg-info/

# Environment
.env
.env.local

# Temporary
*.tmp
*.temp
```

### 6. 민감 정보 확인

다음 항목에 민감 정보가 없는지 확인:
- [ ] API 키 하드코딩 없음
- [ ] 비밀번호 없음
- [ ] 내부 URL 없음
- [ ] 개인 정보 없음

**확인 명령어:**
```bash
# API 키 패턴 검색
grep -r "api.*key\|token\|secret" --include="*.sh" --include="*.yml" .

# 이메일 검색 (공개된 것 제외)
grep -r "@" --include="*.md" --include="*.sh" .
```

### 7. 실행 권한 확인

다음 파일들이 실행 가능해야 합니다:
```bash
chmod +x scripts/scan-sbom.sh
chmod +x docker/entrypoint.sh
chmod +x tests/test-scan.sh
```

### 8. 문서 링크 확인

모든 내부 링크가 작동하는지 확인:
```bash
# README의 모든 링크 확인
grep -o '\[.*\](.*)' README.md
grep -o '\[.*\](.*)' README.ko.md
```

### 9. 최종 테스트

로컬에서 마지막 테스트:
```bash
# 스크립트 도움말 확인
./scripts/scan-sbom.sh --help

# 통합 테스트 실행 (시간 소요)
# ./tests/test-scan.sh
```

## GitHub 저장소 생성

### Option 1: GitHub CLI 사용

```bash
# GitHub에 로그인
gh auth login

# 조직 저장소 생성
gh repo create sktelecom/sbom-tools \
  --public \
  --description "Software Bill of Materials (SBOM) generation tool for supply chain security" \
  --homepage "https://sktelecom.github.io/guide/supply-chain/"

# 생성 확인
gh repo view sktelecom/sbom-tools
```

### Option 2: 웹 UI 사용

1. https://github.com/organizations/sktelecom/repositories/new 접속
2. 저장소 설정:
   - **Repository name**: `sbom-tools`
   - **Description**: `Software Bill of Materials (SBOM) generation tool for supply chain security`
   - **Public** 선택
   - **Initialize this repository**: 체크 안 함 (중요!)
   - **.gitignore**: None (이미 있음)
   - **License**: Apache-2.0 (이미 있음)
3. "Create repository" 클릭

## Git 설정 및 푸시

### 1. 로컬 Git 초기화 (아직 안 했다면)

```bash
cd /mnt/user-data/outputs/sbom-tools

# Git 초기화
git init

# 사용자 설정
git config user.name "Your Name"
git config user.email "your.email@sktelecom.com"
```

### 2. 원격 저장소 연결

```bash
# 원격 저장소 추가
git remote add origin https://github.com/sktelecom/sbom-tools.git

# 또는 SSH 사용
# git remote add origin git@github.com:sktelecom/sbom-tools.git

# 원격 저장소 확인
git remote -v
```

### 3. 파일 정리 및 커밋

```bash
# 백업 파일 삭제
find . -name "*.bak" -type f -delete

# 개발 문서 정리 (선택)
mkdir -p docs/development
mv *_PLAN.md *_STRATEGY.md *_COMPLETE.md *_SUMMARY.md docs/development/ 2>/dev/null

# .gitignore 확인
cat .gitignore

# 모든 파일 추가
git add .

# 상태 확인
git status

# 초기 커밋
git commit -m "feat: Initial release of SBOM Tools v1.0.0

SBOM Tools is a comprehensive solution for automatically generating 
Software Bill of Materials (SBOM) across various programming languages.

Features:
- Multi-language support (Java, Python, Node.js, Ruby, PHP, Rust, Go, .NET, C/C++)
- Multiple analysis modes (source code, Docker images, binaries, RootFS)
- CycloneDX 1.4 standard output
- Docker-based execution (no runtime installation needed)
- Multi-platform support (Linux AMD64/ARM64, macOS)
- Optimized Docker image (3-4 GB, 50% reduction)
- Automated CI/CD workflows
- Comprehensive documentation (English + Korean)
- Example projects for all supported languages

Documentation:
- English README with Korean version
- Getting started guide
- Detailed usage guide
- Contributing guidelines
- Docker deployment guide

Development:
- GitHub Actions CI/CD
- Automated Docker builds
- Integration tests
- Code linting and validation

License: Apache 2.0
Maintainer: SK Telecom Open Source Program Office"
```

### 4. 기본 브랜치 설정 및 푸시

```bash
# 기본 브랜치를 main으로 설정
git branch -M main

# 푸시
git push -u origin main
```

### 5. 첫 릴리스 생성

```bash
# v1.0.0 태그 생성
git tag -a v1.0.0 -m "Release v1.0.0

Initial stable release of SBOM Tools

Features:
- Multi-language SBOM generation (9 languages)
- Source code, Docker image, binary analysis
- CycloneDX 1.4 output format
- Optimized Docker image (3-4 GB)
- Linux AMD64/ARM64 and macOS support
- Automated CI/CD pipelines
- Comprehensive documentation in English and Korean

Technical Details:
- JDK 17 for Java 7-17 support
- Python 3.6+ support
- Node.js 20 runtime
- Docker-based execution
- Multi-platform builds

Documentation:
- README.md (English)
- README.ko.md (Korean)
- Getting started guide
- Usage guide with examples
- Contributing guidelines

Breaking Changes:
- Python 2 support removed (EOL 2020)
- JDK 17 only (removed JDK 8, 11, 21)

Migration:
- Python 2 users: Migrate to Python 3
- Java 21 users: Most code works on JDK 17"

# 태그 푸시
git push origin v1.0.0
```

## 푸시 후 확인 사항

### 1. GitHub 웹에서 확인

https://github.com/sktelecom/sbom-tools 접속하여:
- [ ] README.md가 정상적으로 표시되는지
- [ ] 파일 구조가 올바른지
- [ ] 언어 전환 링크가 작동하는지
- [ ] 모든 배지가 표시되는지

### 2. GitHub Actions 확인

https://github.com/sktelecom/sbom-tools/actions
- [ ] CI 워크플로우가 자동 실행되는지
- [ ] Docker 워크플로우가 실행되는지 (v1.0.0 태그로 인해)
- [ ] Release 워크플로우가 실행되는지

### 3. GitHub Packages 확인

https://github.com/sktelecom/sbom-tools/pkgs/container/sbom-scanner
- [ ] Docker 이미지가 빌드되었는지
- [ ] 태그가 올바른지 (v1.0.0, v1.0, v1, latest)

### 4. GitHub Release 확인

https://github.com/sktelecom/sbom-tools/releases
- [ ] v1.0.0 릴리스가 생성되었는지
- [ ] 릴리스 자산이 업로드되었는지
  - scan-sbom-linux.tar.gz
  - scan-sbom-windows.zip
  - sbom-tools-scripts-v1.0.0.tar.gz
  - sbom-tools-examples-v1.0.0.tar.gz

## 저장소 설정

### Settings → General

**About:**
- Description: `Software Bill of Materials (SBOM) generation tool for supply chain security`
- Website: `https://sktelecom.github.io/guide/supply-chain/`
- Topics: `sbom`, `supply-chain`, `security`, `docker`, `cyclonedx`, `dependency-analysis`, `sktelecom`

**Features:**
- [x] Issues
- [x] Discussions (선택)
- [ ] Wiki (불필요)
- [ ] Projects (선택)

### Settings → Branches

**Branch protection rules (main):**
- [x] Require a pull request before merging
- [x] Require approvals: 1
- [x] Require status checks to pass before merging
  - [x] CI / Integration Test
  - [x] CI / Validate Examples
  - [x] CI / Lint Scripts
- [x] Require conversation resolution before merging
- [ ] Require signed commits (선택)
- [x] Include administrators (선택)

### Settings → Actions → General

**Workflow permissions:**
- [x] Read and write permissions
- [x] Allow GitHub Actions to create and approve pull requests

### Settings → Packages

**Package settings (sbom-scanner):**
- Visibility: Public
- Link to repository: sktelecom/sbom-tools

## 공개 준비

### 1. 소셜 미디어 안내

```markdown
🎉 SK Telecom이 SBOM Tools를 오픈소스로 공개합니다!

소프트웨어 공급망 보안을 위한 SBOM(Software Bill of Materials) 자동 생성 도구

✨ 주요 기능:
- 9개 언어 지원 (Java, Python, Node.js, Ruby, PHP, Rust, Go, .NET, C/C++)
- Docker 기반 (런타임 설치 불필요)
- CycloneDX 1.4 표준
- 멀티 플랫폼 (Linux, macOS)
- 영문/한글 문서 제공

🔗 GitHub: https://github.com/sktelecom/sbom-tools
📚 문서: https://sktelecom.github.io/guide/supply-chain/

#OpenSource #SBOM #SupplyChain #Security #SKTelecom
```

### 2. 내부 공지

팀/조직 내부:
- SBOM Tools 공개 안내
- 사용 방법 교육 자료
- 피드백 수집 채널

### 3. 외부 커뮤니티

- OpenChain Korea
- SBOM 관련 커뮤니티
- 보안 커뮤니티

## 트러블슈팅

### 푸시 실패 시

```bash
# 인증 문제
gh auth login

# 권한 문제
# Organization admin에게 권한 요청

# 네트워크 문제
git config --global http.postBuffer 524288000
```

### Actions 실패 시

1. Actions 탭에서 로그 확인
2. 로컬에서 재현
3. 수정 후 재푸시

## 배포 완료 체크리스트

- [ ] 백업 파일 정리
- [ ] 불필요한 문서 정리
- [ ] Git 초기화
- [ ] 원격 저장소 연결
- [ ] 초기 커밋
- [ ] main 브랜치 푸시
- [ ] v1.0.0 태그 생성 및 푸시
- [ ] GitHub 웹에서 확인
- [ ] Actions 워크플로우 확인
- [ ] Docker 이미지 빌드 확인
- [ ] GitHub Release 확인
- [ ] 저장소 설정 (Description, Topics)
- [ ] Branch protection 설정
- [ ] Actions 권한 설정
- [ ] 패키지 공개 설정
- [ ] 문서 렌더링 확인
- [ ] 링크 작동 확인

---

**준비 되셨으면 시작하세요!** 🚀

위 체크리스트를 하나씩 진행하시면 됩니다.
