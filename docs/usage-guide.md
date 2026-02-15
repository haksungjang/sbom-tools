# 사용 가이드

SBOM Tools의 모든 기능과 사용 시나리오를 다루는 종합 가이드입니다.

## 목차

- [기본 사용법](#기본-사용법)
- [명령줄 옵션](#명령줄-옵션)
- [소스코드 분석](#소스코드-분석)
- [Docker 이미지 분석](#docker-이미지-분석)
- [바이너리 및 펌웨어 분석](#바이너리-및-펌웨어-분석)
- [고급 사용법](#고급-사용법)
- [언어별 상세 가이드](#언어별-상세-가이드)

## 기본 사용법

### 명령 구조

```bash
scan-sbom.sh --project <프로젝트명> --version <버전> [옵션]
```

### 필수 파라미터

| 파라미터 | 설명 | 예시 |
|----------|------|------|
| `--project` | 프로젝트 이름 | `"MyApp"` |
| `--version` | 버전 정보 | `"1.0.0"` |

### 선택 파라미터

| 파라미터 | 설명 | 기본값 |
|----------|------|--------|
| `--target` | 분석 대상 지정 | 현재 디렉토리 |
| `--generate-only` | 로컬 저장만 (업로드 안 함) | - |
| `--help` | 도움말 표시 | - |

## 명령줄 옵션

### --project (필수)

프로젝트 이름을 지정합니다. 생성되는 SBOM 파일명에 포함됩니다.

```bash
--project "MySpringBootApp"
--project "PaymentService"
```

주의사항:
- 공백이 포함된 경우 따옴표로 감싸야 합니다
- 특수문자(`/`, `\`, `:`)는 피하는 것이 좋습니다

### --version (필수)

프로젝트 버전을 지정합니다. Semantic Versioning을 권장합니다.

```bash
--version "1.0.0"
--version "2.1.3-beta"
--version "2024.01.15"
```

### --target (선택)

분석할 대상을 명시적으로 지정합니다.

```bash
# Docker 이미지
--target "nginx:alpine"

# 바이너리 파일
--target "/path/to/firmware.bin"

# 디렉토리
--target "./extracted-rootfs/"
```

미지정 시: 현재 디렉토리의 소스코드를 분석합니다.

### --generate-only (선택)

SBOM을 로컬에만 저장하고 서버에 업로드하지 않습니다.

```bash
--generate-only
```

사용 시나리오:
- 테스트 목적
- 수동 검토 후 제출
- 오프라인 환경

## 소스코드 분석

### 자동 언어 감지

SBOM Tools는 프로젝트 디렉토리의 파일을 분석하여 자동으로 언어를 감지합니다.

감지 방법:

| 언어 | 감지 파일 |
|------|----------|
| Java | `pom.xml`, `build.gradle`, `build.gradle.kts` |
| Python | `requirements.txt`, `setup.py`, `pyproject.toml`, `Pipfile` |
| Node.js | `package.json`, `package-lock.json` |
| Go | `go.mod`, `go.sum` |
| Ruby | `Gemfile`, `Gemfile.lock` |
| PHP | `composer.json`, `composer.lock` |
| Rust | `Cargo.toml`, `Cargo.lock` |
| .NET | `*.csproj`, `*.fsproj`, `*.vbproj`, `packages.config` |

### 기본 실행

```bash
# 프로젝트 디렉토리로 이동
cd /path/to/your/project

# SBOM 생성
scan-sbom.sh --project "ProjectName" --version "1.0.0" --generate-only
```

### 멀티 언어 프로젝트

여러 언어가 혼합된 프로젝트의 경우, 루트 디렉토리에서 실행하면 모든 언어를 자동으로 감지합니다.

```bash
# 모노레포 예시
project/
├── frontend/          # Node.js
│   └── package.json
├── backend/          # Java
│   └── pom.xml
└── worker/           # Python
    └── requirements.txt

# 루트에서 실행
cd project/
scan-sbom.sh --project "FullStackApp" --version "1.0.0" --generate-only
```

결과: 모든 언어의 의존성이 하나의 SBOM에 포함됩니다.

## Docker 이미지 분석

### 로컬 이미지

```bash
# 이미지가 이미 로컬에 존재하는 경우
docker images  # 이미지 목록 확인

scan-sbom.sh \
  --target "myapp:v1.0" \
  --project "MyApp" \
  --version "1.0" \
  --generate-only
```

### 레지스트리 이미지

```bash
# Docker Hub 공개 이미지
scan-sbom.sh \
  --target "nginx:alpine" \
  --project "Nginx" \
  --version "alpine" \
  --generate-only

# GitHub Container Registry
scan-sbom.sh \
  --target "ghcr.io/owner/image:tag" \
  --project "MyImage" \
  --version "1.0" \
  --generate-only
```

참고: 이미지가 로컬에 없으면 자동으로 pull을 시도합니다.

### 프라이빗 레지스트리

사전에 `docker login`이 필요합니다.

```bash
# 1. 레지스트리 로그인
docker login registry.company.com
# Username: your-username
# Password: your-password

# 2. SBOM 생성
scan-sbom.sh \
  --target "registry.company.com/myapp:latest" \
  --project "MyPrivateApp" \
  --version "latest" \
  --generate-only
```

### 이미지 tar 파일

```bash
# Docker 이미지를 tar로 저장
docker save myapp:v1.0 -o myapp.tar

# tar 파일 분석
scan-sbom.sh \
  --target "myapp.tar" \
  --project "MyApp" \
  --version "1.0" \
  --generate-only
```

## 바이너리 및 펌웨어 분석

### 바이너리 파일

실행 파일이나 라이브러리를 분석할 수 있습니다.

```bash
# 펌웨어 파일
scan-sbom.sh \
  --target firmware.bin \
  --project "RouterOS" \
  --version "2.0" \
  --generate-only

# 실행 파일
scan-sbom.sh \
  --target /bin/busybox \
  --project "BusyBox" \
  --version "1.35" \
  --generate-only
```

주의사항:
- 바이너리 분석은 메타데이터 추출에 제한적입니다
- 정적 링크된 라이브러리는 감지가 어렵습니다
- 정확한 SBOM 생성을 위해서는 소스코드 분석을 권장합니다

### RootFS 디렉토리

압축 해제된 파일 시스템을 분석할 수 있습니다.

```bash
# 펌웨어 압축 해제
mkdir rootfs
tar -xf firmware.tar.gz -C rootfs/

# 디렉토리 분석
scan-sbom.sh \
  --target ./rootfs/ \
  --project "DeviceOS" \
  --version "1.0" \
  --generate-only
```

사용 사례:
- 임베디드 시스템 펌웨어
- 컨테이너 파일 시스템 추출
- OS 이미지 분석

## 고급 사용법

### 빌드 캐시 활용

Java 및 Python 프로젝트의 경우 빌드 캐시를 재사용하여 속도를 향상시킬 수 있습니다.

```bash
# Gradle 캐시가 있는 경우 자동으로 마운트됨
ls ~/.gradle/

# Maven 캐시
ls ~/.m2/

# SBOM 생성 시 자동으로 캐시 활용
scan-sbom.sh --project "MyApp" --version "1.0" --generate-only
```

### 프록시 환경

프록시 환경에서 사용하는 경우:

```bash
# 환경변수 설정
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080
export NO_PROXY=localhost,127.0.0.1

# SBOM 생성
scan-sbom.sh --project "MyApp" --version "1.0" --generate-only
```

### CI/CD 통합

#### GitHub Actions

```yaml
name: Generate SBOM

on:
  push:
    branches: [ main ]
  release:
    types: [ published ]

jobs:
  sbom:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Download scan script
        run: |
          curl -O https://raw.githubusercontent.com/sktelecom/sbom-tools/main/scripts/scan-sbom.sh
          chmod +x scan-sbom.sh
      
      - name: Generate SBOM
        run: |
          ./scan-sbom.sh \
            --project "${{ github.repository }}" \
            --version "${{ github.ref_name }}" \
            --generate-only
      
      - name: Upload SBOM
        uses: actions/upload-artifact@v3
        with:
          name: sbom
          path: "*_bom.json"
```

#### GitLab CI

```yaml
generate-sbom:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  script:
    - curl -O https://raw.githubusercontent.com/sktelecom/sbom-tools/main/scripts/scan-sbom.sh
    - chmod +x scan-sbom.sh
    - ./scan-sbom.sh --project "$CI_PROJECT_NAME" --version "$CI_COMMIT_TAG" --generate-only
  artifacts:
    paths:
      - "*_bom.json"
    expire_in: 30 days
```

#### Jenkins

```groovy
pipeline {
    agent any
    stages {
        stage('Generate SBOM') {
            steps {
                sh '''
                    curl -O https://raw.githubusercontent.com/sktelecom/sbom-tools/main/scripts/scan-sbom.sh
                    chmod +x scan-sbom.sh
                    ./scan-sbom.sh --project "${JOB_NAME}" --version "${BUILD_NUMBER}" --generate-only
                '''
                archiveArtifacts artifacts: '*_bom.json', fingerprint: true
            }
        }
    }
}
```

## 언어별 상세 가이드

### Java

#### Maven 프로젝트

필수 파일: `pom.xml`

```bash
cd my-maven-project
scan-sbom.sh --project "MyMavenApp" --version "1.0.0" --generate-only
```

멀티 모듈 프로젝트:

```bash
# 루트 pom.xml이 있는 디렉토리에서 실행
cd multi-module-project/
scan-sbom.sh --project "MultiModuleApp" --version "1.0.0" --generate-only
```

레거시 Java 7 프로젝트:

```xml
<!-- pom.xml -->
<properties>
    <maven.compiler.source>1.7</maven.compiler.source>
    <maven.compiler.target>1.7</maven.compiler.target>
</properties>
```

SBOM Tools는 Java 7-17을 지원합니다 (JDK 17 포함).

> 참고: Docker 이미지에는 JDK 17이 포함되어 있습니다. Java 21 프로젝트는 대부분 JDK 17에서 분석 가능하지만, Java 21 전용 기능을 사용하는 경우 일부 제한이 있을 수 있습니다.

#### Gradle 프로젝트

필수 파일: `build.gradle` 또는 `build.gradle.kts`

```bash
cd my-gradle-project
scan-sbom.sh --project "MyGradleApp" --version "1.0.0" --generate-only
```

Gradle Wrapper:

`gradlew`가 있으면 자동으로 사용됩니다.

```bash
# gradlew 실행 권한은 자동으로 부여됨
scan-sbom.sh --project "MyApp" --version "1.0" --generate-only
```

Kotlin DSL (build.gradle.kts):

Kotlin으로 작성된 빌드 스크립트도 지원됩니다.

### Python

#### pip (requirements.txt)

필수 파일: `requirements.txt`

```bash
cd my-python-project

# requirements.txt 생성 (없는 경우)
pip freeze > requirements.txt

# SBOM 생성
scan-sbom.sh --project "MyPythonApp" --version "1.0.0" --generate-only
```

가상 환경 사용:

```bash
# 가상 환경 생성 및 활성화
python3 -m venv venv
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt

# requirements.txt 업데이트
pip freeze > requirements.txt

# SBOM 생성
scan-sbom.sh --project "MyApp" --version "1.0" --generate-only
```

#### Poetry

필수 파일: `pyproject.toml`, `poetry.lock`

```bash
cd my-poetry-project

# poetry.lock 생성 (없는 경우)
poetry lock

# SBOM 생성
scan-sbom.sh --project "MyPoetryApp" --version "1.0.0" --generate-only
```

#### Pipenv

필수 파일: `Pipfile`, `Pipfile.lock`

```bash
cd my-pipenv-project

# Pipfile.lock 생성
pipenv lock

# SBOM 생성
scan-sbom.sh --project "MyPipenvApp" --version "1.0.0" --generate-only
```

#### Python 2.x (레거시) - 지원 중단

> 중요: Python 2는 2020년에 공식 지원이 종료되었으며, Docker 이미지에서 제거되었습니다. Python 2 프로젝트는 Python 3로 마이그레이션하는 것을 강력히 권장합니다.

대안:
- Python 3로 코드 마이그레이션
- 또는 Python 2가 포함된 커스텀 Docker 이미지 빌드

### Node.js

#### npm

필수 파일: `package.json`, `package-lock.json`

```bash
cd my-nodejs-project

# package-lock.json 생성 (없는 경우)
npm install

# SBOM 생성
scan-sbom.sh --project "MyNodeApp" --version "1.0.0" --generate-only
```

package.json만 있는 경우:

```bash
# lock 파일 생성
npm install --package-lock-only

# SBOM 생성
scan-sbom.sh --project "MyApp" --version "1.0" --generate-only
```

#### Yarn

필수 파일: `package.json`, `yarn.lock`

```bash
cd my-yarn-project

# yarn.lock 생성
yarn install

# SBOM 생성
scan-sbom.sh --project "MyYarnApp" --version "1.0.0" --generate-only
```

#### pnpm

필수 파일: `package.json`, `pnpm-lock.yaml`

```bash
cd my-pnpm-project

# pnpm-lock.yaml 생성
pnpm install

# SBOM 생성
scan-sbom.sh --project "MyPnpmApp" --version "1.0.0" --generate-only
```

### Go

필수 파일: `go.mod`, `go.sum`

```bash
cd my-go-project

# go.sum 생성 (없는 경우)
go mod download

# SBOM 생성
scan-sbom.sh --project "MyGoApp" --version "1.0.0" --generate-only
```

모듈 업데이트:

```bash
# 의존성 정리
go mod tidy

# SBOM 생성
scan-sbom.sh --project "MyApp" --version "1.0" --generate-only
```

### Ruby

필수 파일: `Gemfile`, `Gemfile.lock`

```bash
cd my-ruby-project

# Gemfile.lock 생성
bundle install

# SBOM 생성
scan-sbom.sh --project "MyRubyApp" --version "1.0.0" --generate-only
```

Rails 프로젝트:

```bash
cd my-rails-app

# 프로덕션 의존성만
bundle install --without development test

# SBOM 생성
scan-sbom.sh --project "MyRailsApp" --version "1.0" --generate-only
```

### PHP

필수 파일: `composer.json`, `composer.lock`

```bash
cd my-php-project

# composer.lock 생성
composer install

# SBOM 생성
scan-sbom.sh --project "MyPHPApp" --version "1.0.0" --generate-only
```

Laravel 프로젝트:

```bash
cd my-laravel-app

# 프로덕션 의존성만
composer install --no-dev

# SBOM 생성
scan-sbom.sh --project "MyLaravelApp" --version "1.0" --generate-only
```

### Rust

필수 파일: `Cargo.toml`, `Cargo.lock`

```bash
cd my-rust-project

# Cargo.lock 생성 (없는 경우)
cargo generate-lockfile

# SBOM 생성
scan-sbom.sh --project "MyRustApp" --version "1.0.0" --generate-only
```

Workspace 프로젝트:

```bash
# 루트 Cargo.toml이 있는 디렉토리에서
cd my-rust-workspace
scan-sbom.sh --project "MyWorkspace" --version "1.0" --generate-only
```

### .NET

필수 파일: `*.csproj`, `*.sln`, `packages.config`

```bash
cd my-dotnet-project

# 의존성 복원 (선택)
dotnet restore

# SBOM 생성
scan-sbom.sh --project "MyDotNetApp" --version "1.0.0" --generate-only
```

솔루션 프로젝트:

```bash
# .sln 파일이 있는 디렉토리에서
cd my-solution/
scan-sbom.sh --project "MySolution" --version "1.0" --generate-only
```

### C/C++

C/C++ 프로젝트는 패키지 매니저를 사용하는 경우에만 분석 가능합니다.

#### Conan

필수 파일: `conanfile.txt` 또는 `conanfile.py`

```bash
cd my-cpp-project

# conanfile.txt 예시
cat > conanfile.txt <<EOF
[requires]
boost/1.80.0
openssl/3.0.0

[generators]
cmake
EOF

# SBOM 생성
scan-sbom.sh --project "MyCppApp" --version "1.0.0" --generate-only
```

#### vcpkg (제한적)

vcpkg는 제한적으로 지원됩니다.

주의: 헤더 파일만 사용하는 프로젝트나 직접 의존성을 관리하는 경우 SBOM 생성이 제한적일 수 있습니다.

## 출력 형식

### CycloneDX 1.4

생성되는 SBOM은 CycloneDX 1.4 형식의 JSON 파일입니다.

파일 구조:

```json
{
  "bomFormat": "CycloneDX",
  "specVersion": "1.4",
  "serialNumber": "urn:uuid:...",
  "version": 1,
  "metadata": {
    "timestamp": "2024-01-15T10:30:00Z",
    "tools": [{
      "vendor": "CycloneDX",
      "name": "cdxgen",
      "version": "10.0.0"
    }],
    "component": {
      "type": "application",
      "name": "MyApp",
      "version": "1.0.0"
    }
  },
  "components": [
    {
      "type": "library",
      "name": "express",
      "version": "4.18.2",
      "purl": "pkg:npm/express@4.18.2",
      "licenses": [...]
    }
  ]
}
```

### 파일명 규칙

생성되는 SBOM 파일명:

```
{ProjectName}_{Version}_bom.json
```

예시:
- `MyApp_1.0.0_bom.json`
- `PaymentService_2.1.3_bom.json`

특수문자 처리:
- 공백 및 특수문자는 언더스코어(`_`)로 변환됩니다
- 연속된 언더스코어는 하나로 축약됩니다

## 다음 단계

- [예제 프로젝트](../examples/): 언어별 샘플 프로젝트
- [Docker 이미지 가이드](../docker/README.md): Docker 이미지 직접 빌드
- [GitHub 이슈](https://github.com/sktelecom/sbom-tools/issues): 문제 보고 및 기능 제안

## 도움말

문의사항이나 문제가 있으신 경우:

- 이메일: opensource@sktelecom.com
- 이슈: [GitHub Issues](https://github.com/sktelecom/sbom-tools/issues)
- 공식 가이드: https://sktelecom.github.io/guide/supply-chain/
