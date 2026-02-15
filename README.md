# SBOM Tools

> Automated Software Bill of Materials (SBOM) generation tool for supply chain security

[![GitHub release](https://img.shields.io/github/v/release/sktelecom/sbom-tools?style=flat-square)](https://github.com/sktelecom/sbom-tools/releases)
[![Docker Pulls](https://img.shields.io/docker/pulls/sktelecom/sbom-scanner?style=flat-square)](https://github.com/sktelecom/sbom-tools/pkgs/container/sbom-scanner)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg?style=flat-square)](LICENSE)

## Overview

SBOM Tools automatically generates Software Bill of Materials (SBOM) in CycloneDX format for multiple programming languages and environments. Developed by SK Telecom for supply chain security management, now available as open source.

### Key Features

- **Multi-language Support**: Java, Python, Node.js, Ruby, PHP, Rust, Go, .NET, C/C++
- **Versatile Analysis Modes**: Source code, Docker images, binary files, RootFS
- **Standard Format**: CycloneDX 1.4
- **Docker-based**: No language-specific runtime installation required
- **Cross-platform**: Linux (AMD64, ARM64), macOS, Windows

### Supported Languages

| Language | Package Managers | Analysis Tools |
|----------|------------------|----------------|
| **Java** | Maven, Gradle | cdxgen |
| **Python** | pip, Poetry | cdxgen |
| **Node.js** | npm, Yarn, pnpm | cdxgen |
| **Ruby** | Bundler | cdxgen |
| **PHP** | Composer | cdxgen |
| **Rust** | Cargo | cdxgen |
| **Go** | Go modules | cdxgen |
| **.NET** | NuGet | cdxgen |
| **Docker** | - | syft |
| **Binary** | - | syft |

## Quick Start

### Prerequisites

- Docker 20.10 or higher
- 4GB+ available disk space

### Installation

```bash
# Pull the Docker image
docker pull ghcr.io/sktelecom/sbom-scanner:latest
```

### Basic Usage

#### 1. Scan Source Code

```bash
# Navigate to your project directory
cd /path/to/your/project

# Generate SBOM
./scripts/scan-sbom.sh --project "MyApp" --version "1.0.0" --generate-only
```

#### 2. Scan Docker Image

```bash
./scripts/scan-sbom.sh \
  --project "MyApp" \
  --version "1.0.0" \
  --target "nginx:latest" \
  --generate-only
```

#### 3. Scan Binary File

```bash
./scripts/scan-sbom.sh \
  --project "MyApp" \
  --version "1.0.0" \
  --target "./firmware.bin" \
  --generate-only
```

### Output

Generated SBOM file: `{ProjectName}_{Version}_bom.json`

```json
{
  "bomFormat": "CycloneDX",
  "specVersion": "1.4",
  "version": 1,
  "metadata": {
    "component": {
      "name": "MyApp",
      "version": "1.0.0"
    }
  },
  "components": [
    {
      "type": "library",
      "name": "express",
      "version": "4.18.2",
      "purl": "pkg:npm/express@4.18.2"
    }
  ]
}
```

## Documentation

### For Users (Korean)

- **[시작하기](docs/getting-started.md)** - 설치 및 기본 사용법
- **[사용 가이드](docs/usage-guide.md)** - 상세 사용 방법
- **[예제 가이드](docs/examples-guide.md)** - 언어별 예제 프로젝트

### For Contributors (Korean)

- **[아키텍처](docs/architecture.ko.md)** - 시스템 구조 및 설계
- **[패키지 매니저 추가](docs/contributing/package-manager-guide.ko.md)** - 새로운 언어 지원 추가
- **[테스트 가이드](docs/contributing/testing-guide.ko.md)** - 테스트 작성 및 실행
- **[테스트 로깅](docs/contributing/test-logging-guide.ko.md)** - 테스트 디버깅

## Examples

The `examples/` directory contains sample projects for each supported language:

```
examples/
├── java-maven/      # Java with Maven
├── java-gradle/     # Java with Gradle
├── nodejs/          # Node.js with npm
├── python/          # Python with pip
├── go/              # Go modules
├── ruby/            # Ruby with Bundler
├── php/             # PHP with Composer
├── rust/            # Rust with Cargo
├── dotnet/          # .NET with NuGet
└── docker/          # Docker image analysis
```

Try an example:

```bash
cd examples/nodejs
../../scripts/scan-sbom.sh --project "NodeExample" --version "1.0.0" --generate-only
```

## Architecture

```
┌─────────────────────────────────────────────────┐
│              scan-sbom.sh (Wrapper)             │
└────────────────────┬────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────┐
│         Docker Container (SBOM Scanner)         │
│  ┌──────────────────────────────────────────┐  │
│  │  Multi-language Runtime Environment      │  │
│  │  • JDK 17  • Python 3  • Node.js 20      │  │
│  │  • Ruby    • PHP       • Rust            │  │
│  │  • Go      • .NET      • Build Tools     │  │
│  └──────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────┐  │
│  │  SBOM Generation Tools                   │  │
│  │  • cdxgen (source code)                  │  │
│  │  • syft (images/binaries)                │  │
│  └──────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
                     │
                     ▼
              CycloneDX SBOM File
```

See [docs/architecture.ko.md](docs/architecture.ko.md) for detailed architecture (Korean).

## Testing

Run integration tests:

```bash
# Normal mode (quiet)
./tests/test-scan.sh

# Verbose mode (show key messages)
VERBOSE=true ./tests/test-scan.sh

# Debug mode (show all output)
DEBUG_MODE=true ./tests/test-scan.sh
```

## Contributing

We welcome contributions! See [docs/contributing/](docs/contributing/) for guides (Korean).

### Quick Links

- Report bugs: [GitHub Issues](https://github.com/haksungjang/sbom-tools/issues)
- Suggest features: [GitHub Discussions](https://github.com/haksungjang/sbom-tools/discussions)
- Submit code: [Pull Requests](https://github.com/haksungjang/sbom-tools/pulls)

## License

Apache License 2.0

Copyright 2026 SK Telecom Co., Ltd.

## Contact

- **Email**: opensource@sktelecom.com
- **GitHub**: https://github.com/haksungjang/sbom-tools

## Acknowledgments

This project uses:
- [CycloneDX](https://cyclonedx.org/) - SBOM standard
- [cdxgen](https://github.com/CycloneDX/cdxgen) - Source code analysis
- [Syft](https://github.com/anchore/syft) - Container/binary analysis

---

Made with ❤️ by SK Telecom Open Source Team
