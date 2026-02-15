# 시작하기

SBOM Tools를 처음 사용하는 분들을 위한 단계별 가이드입니다.

## 목차

- [사전 요구사항](#사전-요구사항)
- [설치](#설치)
- [첫 SBOM 생성](#첫-sbom-생성)
- [생성된 SBOM 확인](#생성된-sbom-확인)
- [문제 해결](#문제-해결)

## 사전 요구사항

### Docker 설치

SBOM Tools는 Docker를 사용하므로, Docker가 설치되어 있어야 합니다.

#### Linux

```bash
# Docker 설치 (Ubuntu/Debian)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 현재 사용자를 docker 그룹에 추가
sudo usermod -aG docker $USER

# 로그아웃 후 다시 로그인
```

#### macOS

Docker Desktop for Mac을 설치합니다:
- https://docs.docker.com/desktop/install/mac-install/

#### Windows

Docker Desktop for Windows를 설치합니다:
- https://docs.docker.com/desktop/install/windows-install/

WSL2 사용 권장: Windows에서는 WSL2 환경에서 사용하는 것을 권장합니다.

### 설치 확인

```bash
# Docker 버전 확인
docker --version
# 출력 예시: Docker version 24.0.7, build afdd53b

# Docker 실행 확인
docker ps
# 오류 없이 실행되어야 함
```

Docker 데몬이 실행 중이지 않다면:

```bash
# Linux
sudo systemctl start docker

# macOS/Windows
# Docker Desktop 애플리케이션 실행
```

## 설치

### 방법 1: 스크립트 다운로드 (권장)

```bash
# 스크립트 다운로드
curl -O https://raw.githubusercontent.com/sktelecom/sbom-tools/main/scripts/scan-sbom.sh

# 실행 권한 부여
chmod +x scan-sbom.sh

# 확인
./scan-sbom.sh --help
```

### 방법 2: 저장소 클론

```bash
# 저장소 클론
git clone https://github.com/sktelecom/sbom-tools.git
cd sbom-tools

# 스크립트로 이동
cd scripts
chmod +x scan-sbom.sh

# 확인
./scan-sbom.sh --help
```

### 방법 3: Docker 이미지만 사용

스크립트 없이 Docker 이미지를 직접 사용할 수도 있습니다:

```bash
# Docker 이미지 다운로드
docker pull ghcr.io/sktelecom/sbom-scanner:v1

# 확인
docker images | grep sbom-scanner
```

## 첫 SBOM 생성

### 1단계: 테스트 프로젝트 준비

간단한 테스트 프로젝트를 만들어 봅니다.

#### Node.js 프로젝트 예시

```bash
# 테스트 디렉토리 생성
mkdir ~/sbom-test
cd ~/sbom-test

# package.json 생성
cat > package.json <<EOF
{
  "name": "test-app",
  "version": "1.0.0",
  "dependencies": {
    "express": "^4.18.0",
    "lodash": "^4.17.21"
  }
}
EOF

# package-lock.json 생성
npm install --package-lock-only
```

#### Python 프로젝트 예시

```bash
# 테스트 디렉토리 생성
mkdir ~/sbom-test-python
cd ~/sbom-test-python

# requirements.txt 생성
cat > requirements.txt <<EOF
requests==2.31.0
flask==3.0.0
numpy==1.26.0
EOF
```

#### Java Maven 프로젝트 예시

```bash
# 테스트 디렉토리 생성
mkdir ~/sbom-test-java
cd ~/sbom-test-java

# pom.xml 생성
cat > pom.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>test-app</artifactId>
    <version>1.0.0</version>
    
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
            <version>3.2.0</version>
        </dependency>
    </dependencies>
</project>
EOF
```

### 2단계: SBOM 생성 실행

```bash
# scan-sbom.sh가 있는 위치로 이동하거나 PATH에 추가한 후
cd ~/sbom-test

# SBOM 생성 (스크립트 경로 지정)
/path/to/scan-sbom.sh --project "TestApp" --version "1.0.0" --generate-only
```

출력 예시:
```
==========================================
 Starting SBOM Analysis
 Mode: SOURCE
 Project: TestApp (1.0.0)
==========================================
[1/2] Analyzing Source Code...
[INFO] SBOM generated: TestApp_1.0.0_bom.json
[INFO] Generate-only mode.
[SUCCESS] SBOM copied to: /current/directory/TestApp_1.0.0_bom.json
==========================================
 Analysis Complete!
 SBOM saved: TestApp_1.0.0_bom.json
==========================================
```

### 3단계: 다른 대상 유형 테스트

#### Docker 이미지

```bash
# Alpine Linux 이미지 분석
/path/to/scan-sbom.sh \
  --target "alpine:latest" \
  --project "AlpineTest" \
  --version "latest" \
  --generate-only
```

참고: 이미지가 로컬에 없으면 자동으로 다운로드됩니다.

#### 바이너리 파일

```bash
# /bin/ls 바이너리 분석 (예시)
/path/to/scan-sbom.sh \
  --target /bin/ls \
  --project "LSCommand" \
  --version "1.0" \
  --generate-only
```

## 생성된 SBOM 확인

### 파일 크기 및 위치

```bash
# 생성된 파일 확인
ls -lh *_bom.json

# 출력 예시:
# -rw-r--r--  1 user  staff   45K Jan 15 10:30 TestApp_1.0.0_bom.json
```

정상 파일 크기: 최소 1KB 이상 (프로젝트 규모에 따라 다름)

### 파일 내용 확인

```bash
# JSON 유효성 확인 (jq 필요)
cat TestApp_1.0.0_bom.json | jq empty

# 기본 정보 확인
cat TestApp_1.0.0_bom.json | jq '{
  bomFormat,
  specVersion,
  projectName: .metadata.component.name,
  components: (.components | length)
}'
```

출력 예시:
```json
{
  "bomFormat": "CycloneDX",
  "specVersion": "1.4",
  "projectName": "TestApp",
  "components": 42
}
```

### 컴포넌트 목록 확인

```bash
# 컴포넌트 이름과 버전 목록
cat TestApp_1.0.0_bom.json | jq -r '.components[] | "\(.name)@\(.version)"' | head -10
```

출력 예시:
```
express@4.18.2
lodash@4.17.21
body-parser@1.20.1
cookie@0.5.0
debug@2.6.9
...
```

### 온라인 검증

CycloneDX 공식 검증 도구로 SBOM 유효성을 확인할 수 있습니다:

1. https://cyclonedx.github.io/cyclonedx-web-tool/validate 접속
2. 생성된 `bom.json` 파일 업로드
3. 검증 결과 확인

## 문제 해결

### Docker 관련 오류

#### 오류: "docker: command not found"

원인: Docker가 설치되지 않음

해결:
```bash
# Docker 설치
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

#### 오류: "Cannot connect to the Docker daemon"

원인: Docker 데몬이 실행 중이지 않음

해결:
```bash
# Linux
sudo systemctl start docker
sudo systemctl enable docker

# macOS/Windows
# Docker Desktop 애플리케이션 실행
```

#### 오류: "permission denied while trying to connect"

원인: 현재 사용자가 docker 그룹에 속하지 않음

해결:
```bash
# 사용자를 docker 그룹에 추가
sudo usermod -aG docker $USER

# 로그아웃 후 다시 로그인
# 또는 임시로:
newgrp docker
```

### 스크립트 실행 오류

#### 오류: "Permission denied: ./scan-sbom.sh"

원인: 실행 권한 없음

해결:
```bash
chmod +x scan-sbom.sh
```

#### 오류: "bash: ./scan-sbom.sh: /bin/bash^M: bad interpreter"

원인: Windows에서 작성된 파일의 줄바꿈 문제 (CRLF)

해결:
```bash
# dos2unix 설치 및 변환
sudo apt-get install dos2unix  # Ubuntu/Debian
dos2unix scan-sbom.sh

# 또는 sed 사용
sed -i 's/\r$//' scan-sbom.sh
```

### SBOM 생성 실패

#### 증상: "SBOM file is empty or not generated"

원인 1: 프로젝트에 의존성 파일이 없음

해결:
```bash
# Node.js
npm install  # package-lock.json 생성

# Python
pip freeze > requirements.txt

# Maven
mvn dependency:tree  # 의존성 확인
```

원인 2: 잘못된 디렉토리에서 실행

해결:
```bash
# package.json, pom.xml, requirements.txt 등이 있는 디렉토리에서 실행
cd /path/to/project/root
/path/to/scan-sbom.sh --project "MyApp" --version "1.0" --generate-only
```

#### 증상: "No components found in SBOM"

원인: 의존성이 실제로 없거나 매우 적음

확인:
```bash
# package.json 확인
cat package.json

# dependencies 섹션이 있는지 확인
jq '.dependencies' package.json
```

### Docker 이미지 다운로드 실패

#### 오류: "Error response from daemon: Get https://ghcr.io/v2/"

원인: 네트워크 연결 문제 또는 프록시 설정

해결:
```bash
# 인터넷 연결 확인
ping google.com

# Docker 이미지 수동 다운로드 재시도
docker pull ghcr.io/sktelecom/sbom-scanner:v1

# 프록시 설정 (필요한 경우)
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080
```

### 특정 언어 지원 문제

#### Java 프로젝트가 분석되지 않음

확인 사항:
```bash
# pom.xml 또는 build.gradle이 있는지 확인
ls -la pom.xml build.gradle

# XML 문법 오류 확인
xmllint --noout pom.xml 2>&1
```

#### Python 2.x 프로젝트 (지원 중단)

> 중요: Python 2는 2020년에 공식 지원이 종료되었으며, v1.0.0부터 Docker 이미지에서 제거되었습니다. Python 2 프로젝트는 Python 3로 마이그레이션하는 것을 권장합니다.

레거시 프로젝트를 위한 대안:
- Python 3로 코드 마이그레이션 (권장)
- Python 2가 포함된 커스텀 Docker 이미지 빌드

## 다음 단계

SBOM을 성공적으로 생성했다면, 다음 문서를 참고하세요:

- [사용 가이드](usage-guide.md): 언어별 상세 사용법 및 고급 기능
- [예제 프로젝트](../examples/): 언어별 예제 프로젝트
- [Docker 이미지 가이드](../docker/README.md): Docker 이미지 직접 빌드 및 배포

## 도움이 필요하신가요?

- 이슈 제출: [GitHub Issues](https://github.com/sktelecom/sbom-tools/issues)
- 이메일 문의: opensource@sktelecom.com
- 공식 가이드: https://sktelecom.github.io/guide/supply-chain/
