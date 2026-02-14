# SBOM Tools

**🇰🇷 한국어** | **[🇺🇸 English](README.md)**

> 공급망 보안을 위한 SBOM 생성 도구

[![GitHub release](https://img.shields.io/github/v/release/sktelecom/sbom-tools?style=flat-square)](https://github.com/sktelecom/sbom-tools/releases)
[![Docker Pulls](https://img.shields.io/docker/pulls/sktelecom/sbom-scanner?style=flat-square)](https://github.com/sktelecom/sbom-tools/pkgs/container/sbom-scanner)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg?style=flat-square)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/sktelecom/sbom-tools?style=flat-square)](https://github.com/sktelecom/sbom-tools/stargazers)

## 소개

SBOM Tools는 다양한 프로그래밍 언어와 환경에서 SBOM(Software Bill of Materials)을 자동으로 생성하는 도구입니다. SK텔레콤이 공급망 보안 강화를 위해 개발하였으며, 오픈소스로 공개하여 누구나 사용할 수 있습니다.

### 주요 기능

- **다중 언어 지원**: Java, Python, Node.js, Ruby, PHP, Rust, Go, .NET, C/C++
- **다양한 대상 분석**: 소스코드, Docker 이미지, 바이너리 파일, RootFS
- **표준 형식 출력**: CycloneDX 1.4 형식 SBOM 생성
- **Docker 기반**: 별도 언어 런타임 설치 불필요
- **멀티 플랫폼**: Linux (AMD64, ARM64), macOS 지원

### 지원 언어

| 언어 | 패키지 매니저 | 지원 버전 |
|------|--------------|----------|
| **Java** | Maven, Gradle | Java 7-17 (JDK 17) |
| **Python** | pip, Poetry, Pipenv | Python 3.6+ |
| **Node.js** | npm, Yarn, pnpm | Node.js 14+ |
| **Ruby** | Bundler | Ruby 2.x, 3.x |
| **PHP** | Composer | PHP 7.x, 8.x |
| **Rust** | Cargo | Rust 1.x |
| **Go** | Go modules | Go 1.16+ |
| **.NET** | NuGet | .NET Core, .NET 5+ |
| **C/C++** | Conan, vcpkg | - |

> **참고:** Docker 이미지에는 JDK 17이 포함되어 있어 Java 7-17로 빌드된 프로젝트를 분석할 수 있습니다. Java 21 프로젝트 또는 Python 2.x 레거시 프로젝트는 [사용 가이드](docs/usage-guide.md)를 참고하세요.

## Quick Start

### 1. 사전 요구사항

- **Docker**: 20.10 이상 ([설치 가이드](https://docs.docker.com/get-docker/))

```bash
# Docker 설치 확인
docker --version
```

### 2. 스크립트 다운로드

```bash
# 스크립트 다운로드
curl -O https://raw.githubusercontent.com/sktelecom/sbom-tools/main/scripts/scan-sbom.sh
chmod +x scan-sbom.sh
```

### 3. SBOM 생성

```bash
# 현재 디렉토리의 소스코드 분석
cd /path/to/your/project
./scan-sbom.sh --project "MyApp" --version "1.0.0" --generate-only
```

**결과**: `MyApp_1.0.0_bom.json` 파일 생성

## 사용 예시

### 소스코드 분석

```bash
# Java Maven 프로젝트
cd my-java-app
scan-sbom.sh --project "JavaApp" --version "1.0.0" --generate-only

# Python 프로젝트
cd my-python-app
scan-sbom.sh --project "PythonApp" --version "1.0.0" --generate-only

# Node.js 프로젝트
cd my-nodejs-app
scan-sbom.sh --project "NodeApp" --version "1.0.0" --generate-only
```

### Docker 이미지 분석

```bash
# 로컬 이미지 분석
scan-sbom.sh --target "myapp:latest" --project "MyApp" --version "1.0" --generate-only

# 레지스트리 이미지 분석
scan-sbom.sh --target "nginx:alpine" --project "Nginx" --version "alpine" --generate-only
```

### 바이너리/펌웨어 분석

```bash
# 펌웨어 파일 분석
scan-sbom.sh --target firmware.bin --project "RouterOS" --version "2.0" --generate-only

# RootFS 디렉토리 분석
scan-sbom.sh --target ./rootfs/ --project "DeviceOS" --version "1.0" --generate-only
```

## 고급 사용법

### Docker 이미지 버전 관리

기본적으로 스크립트는 `latest` Docker 이미지를 사용합니다. 프로덕션 환경에서는 특정 버전으로 고정할 수 있습니다:

```bash
# 최신 릴리스 사용 (기본값)
./scan-sbom.sh --project "MyApp" --version "1.0.0" --generate-only

# v1 패밀리로 고정 (최신 v1.x.x)
SBOM_SCANNER_IMAGE=ghcr.io/sktelecom/sbom-scanner:v1 \
  ./scan-sbom.sh --project "MyApp" --version "1.0.0" --generate-only

# 정확한 버전으로 고정 (프로덕션 권장)
SBOM_SCANNER_IMAGE=ghcr.io/sktelecom/sbom-scanner:v1.0.0 \
  ./scan-sbom.sh --project "MyApp" --version "1.0.0" --generate-only
```

**버전 전략:**
- `latest` - 항상 최신 기능 사용 (개발 환경 권장)
- `v1` - 최신 v1.x.x 릴리스 (CI/CD 권장)
- `v1.0` - 최신 v1.0.x 패치 (안정적인 프로덕션 권장)
- `v1.0.0` - 정확한 버전 (최대 안정성)

### Windows 사용법

```cmd
REM 스크립트 다운로드
curl -O https://raw.githubusercontent.com/sktelecom/sbom-tools/main/scripts/scan-sbom.bat

REM 기본 사용
scan-sbom.bat --project "MyApp" --version "1.0.0" --generate-only

REM 특정 버전으로 고정
set SBOM_SCANNER_IMAGE=ghcr.io/sktelecom/sbom-scanner:v1
scan-sbom.bat --project "MyApp" --version "1.0.0" --generate-only
```

## 문서

- **[시작하기](docs/getting-started.md)**: 상세한 설치 및 첫 사용 가이드
- **[사용 가이드](docs/usage-guide.md)**: 언어별 상세 사용법 및 고급 기능
- **[Docker 이미지](docker/README.md)**: Docker 이미지 빌드 및 배포

## 아키텍처

```
┌─────────────────────────────────────────────────────┐
│                  scan-sbom.sh                       │
│              (사용자 인터페이스)                      │
└─────────────────────┬───────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────┐
│         ghcr.io/sktelecom/sbom-scanner:v1           │
│                (Docker 컨테이너)                     │
│  ┌──────────────────────────────────────────────┐  │
│  │           entrypoint.sh                      │  │
│  │     (분석 로직 및 도구 실행)                  │  │
│  └──────────────────────────────────────────────┘  │
│                      │                              │
│        ┌─────────────┼─────────────┐               │
│        │             │             │               │
│        ▼             ▼             ▼               │
│   ┌────────┐   ┌────────┐   ┌────────┐            │
│   │cdxgen  │   │ syft   │   │ trivy  │            │
│   │(소스)  │   │(이미지)│   │(이미지)│            │
│   └────────┘   └────────┘   └────────┘            │
└─────────────────────────────────────────────────────┘
                      │
                      ▼
          ┌───────────────────────┐
          │   bom.json (출력)     │
          │  (CycloneDX 1.4)      │
          └───────────────────────┘
```

## 기여

프로젝트 개선에 기여하고 싶으시다면 [기여 가이드라인](CONTRIBUTING.md)을 참고해주세요.

### 이슈 제출

버그 리포트나 기능 제안은 [GitHub Issues](https://github.com/sktelecom/sbom-tools/issues)에 등록해주세요.

### Pull Request

1. 저장소를 Fork합니다
2. 기능 브랜치를 생성합니다 (`git checkout -b feature/amazing-feature`)
3. 변경사항을 커밋합니다 (`git commit -m 'Add amazing feature'`)
4. 브랜치에 Push합니다 (`git push origin feature/amazing-feature`)
5. Pull Request를 생성합니다

## 라이선스

Copyright © 2026 SK Telecom Co., Ltd. All Rights Reserved.

본 프로젝트는 [Apache License 2.0](LICENSE) 라이선스 하에 배포됩니다.

```
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

## 지원

- **이메일**: opensource@sktelecom.com
- **이슈 트래커**: [GitHub Issues](https://github.com/sktelecom/sbom-tools/issues)
- **가이드 문서**: https://sktelecom.github.io/guide/supply-chain/

## 관련 프로젝트

- [CycloneDX](https://cyclonedx.org/) - SBOM 표준 형식
- [cdxgen](https://github.com/CycloneDX/cdxgen) - SBOM 생성 도구
- [Syft](https://github.com/anchore/syft) - 컨테이너 이미지 분석 도구
- [Dependency-Track](https://dependencytrack.org/) - SBOM 분석 플랫폼

## 감사의 말

본 프로젝트는 다음 오픈소스 프로젝트들을 활용합니다:

- [CycloneDX cdxgen](https://github.com/CycloneDX/cdxgen) - Apache 2.0
- [Anchore Syft](https://github.com/anchore/syft) - Apache 2.0
- [Aqua Security Trivy](https://github.com/aquasecurity/trivy) - Apache 2.0

---

Made by SK Telecom Open Source Program Office