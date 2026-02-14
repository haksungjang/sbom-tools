# SBOM Tools

**[🇰🇷 한국어](README.ko.md)** | **🇺🇸 English**

> Software Bill of Materials (SBOM) generation tool for supply chain security

[![GitHub release](https://img.shields.io/github/v/release/sktelecom/sbom-tools?style=flat-square)](https://github.com/sktelecom/sbom-tools/releases)
[![Docker Pulls](https://img.shields.io/docker/pulls/sktelecom/sbom-scanner?style=flat-square)](https://github.com/sktelecom/sbom-tools/pkgs/container/sbom-scanner)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg?style=flat-square)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/sktelecom/sbom-tools?style=flat-square)](https://github.com/sktelecom/sbom-tools/stargazers)

## Overview

SBOM Tools is a comprehensive solution for automatically generating Software Bill of Materials (SBOM) across various programming languages and environments. Developed by SK Telecom to enhance supply chain security, it's now open-sourced for everyone to use.

### Key Features

- **Multi-language Support**: Java, Python, Node.js, Ruby, PHP, Rust, Go, .NET, C/C++
- **Versatile Analysis**: Source code, Docker images, binary files, RootFS
- **Standard Format**: Generates CycloneDX 1.4 format SBOM
- **Docker-based**: No need to install language-specific runtimes
- **Multi-platform**: Supports Linux (AMD64, ARM64) and macOS

### Supported Languages

| Language | Package Manager | Supported Versions |
|----------|----------------|-------------------|
| **Java** | Maven, Gradle | Java 7-17 (JDK 17) |
| **Python** | pip, Poetry, Pipenv | Python 3.6+ |
| **Node.js** | npm, Yarn, pnpm | Node.js 14+ |
| **Ruby** | Bundler | Ruby 2.x, 3.x |
| **PHP** | Composer | PHP 7.x, 8.x |
| **Rust** | Cargo | Rust 1.x |
| **Go** | Go modules | Go 1.16+ |
| **.NET** | NuGet | .NET Core, .NET 5+ |
| **C/C++** | Conan, vcpkg | - |

> **Note:** The Docker image includes JDK 17, which supports analysis of projects built with Java 7-17. For Java 21 projects or Python 2.x legacy projects, please refer to the [documentation](docs/usage-guide.md).

## Quick Start

### 1. Prerequisites

- **Docker**: 20.10 or higher ([Installation Guide](https://docs.docker.com/get-docker/))

```bash
# Verify Docker installation
docker --version
```

### 2. Download Script

```bash
# Download the script
curl -O https://raw.githubusercontent.com/sktelecom/sbom-tools/main/scripts/scan-sbom.sh
chmod +x scan-sbom.sh
```

### 3. Generate SBOM

```bash
# Analyze source code in current directory
cd /path/to/your/project
./scan-sbom.sh --project "MyApp" --version "1.0.0" --generate-only
```

**Result**: Generates `MyApp_1.0.0_bom.json`

## Usage Examples

### Source Code Analysis

```bash
# Java Maven project
cd my-java-app
scan-sbom.sh --project "JavaApp" --version "1.0.0" --generate-only

# Python project
cd my-python-app
scan-sbom.sh --project "PythonApp" --version "1.0.0" --generate-only

# Node.js project
cd my-nodejs-app
scan-sbom.sh --project "NodeApp" --version "1.0.0" --generate-only
```

### Docker Image Analysis

```bash
# Analyze local image
scan-sbom.sh --target "myapp:latest" --project "MyApp" --version "1.0" --generate-only

# Analyze registry image
scan-sbom.sh --target "nginx:alpine" --project "Nginx" --version "alpine" --generate-only
```

### Binary/Firmware Analysis

```bash
# Analyze firmware file
scan-sbom.sh --target firmware.bin --project "RouterOS" --version "2.0" --generate-only

# Analyze RootFS directory
scan-sbom.sh --target ./rootfs/ --project "DeviceOS" --version "1.0" --generate-only
```

## Advanced Usage

### Docker Image Version Control

By default, the script uses the `latest` Docker image. You can pin to a specific version for production use:

```bash
# Use latest release (default)
./scan-sbom.sh --project "MyApp" --version "1.0.0" --generate-only

# Pin to v1 family (latest v1.x.x)
SBOM_SCANNER_IMAGE=ghcr.io/sktelecom/sbom-scanner:v1 \
  ./scan-sbom.sh --project "MyApp" --version "1.0.0" --generate-only

# Pin to exact version for production
SBOM_SCANNER_IMAGE=ghcr.io/sktelecom/sbom-scanner:v1.0.0 \
  ./scan-sbom.sh --project "MyApp" --version "1.0.0" --generate-only
```

**Version Strategy:**
- `latest` - Always get the newest features (recommended for development)
- `v1` - Latest v1.x.x release (recommended for CI/CD)
- `v1.0` - Latest v1.0.x patch (recommended for stable production)
- `v1.0.0` - Exact version (maximum stability)

### Windows Usage

```cmd
REM Download script
curl -O https://raw.githubusercontent.com/sktelecom/sbom-tools/main/scripts/scan-sbom.bat

REM Default usage
scan-sbom.bat --project "MyApp" --version "1.0.0" --generate-only

REM Pin to specific version
set SBOM_SCANNER_IMAGE=ghcr.io/sktelecom/sbom-scanner:v1
scan-sbom.bat --project "MyApp" --version "1.0.0" --generate-only
```

## Documentation

- **[Getting Started](docs/getting-started.md)**: Detailed installation and first-use guide (Korean)
- **[Usage Guide](docs/usage-guide.md)**: Language-specific usage and advanced features (Korean)
- **[Docker Image](docker/README.md)**: Docker image build and deployment (Korean)

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                  scan-sbom.sh                       │
│                (User Interface)                      │
└─────────────────────┬───────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────┐
│         ghcr.io/sktelecom/sbom-scanner:v1           │
│                (Docker Container)                    │
│  ┌──────────────────────────────────────────────┐  │
│  │           entrypoint.sh                      │  │
│  │     (Analysis Logic & Tool Execution)        │  │
│  └──────────────────────────────────────────────┘  │
│                      │                              │
│        ┌─────────────┼─────────────┐               │
│        │             │             │               │
│        ▼             ▼             ▼               │
│   ┌────────┐   ┌────────┐   ┌────────┐            │
│   │cdxgen  │   │ syft   │   │ trivy  │            │
│   │(Source)│   │(Image) │   │(Image) │            │
│   └────────┘   └────────┘   └────────┘            │
└─────────────────────────────────────────────────────┘
                      │
                      ▼
          ┌───────────────────────┐
          │   bom.json (Output)   │
          │   (CycloneDX 1.4)     │
          └───────────────────────┘
```

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) (Korean) for details.

### Reporting Issues

Report bugs or suggest features via [GitHub Issues](https://github.com/sktelecom/sbom-tools/issues).

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

Copyright © 2026 SK Telecom Co., Ltd. All Rights Reserved.

This project is distributed under the [Apache License 2.0](LICENSE).

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

## Support

- **Email**: opensource@sktelecom.com
- **Issue Tracker**: [GitHub Issues](https://github.com/sktelecom/sbom-tools/issues)
- **Documentation**: https://sktelecom.github.io/guide/supply-chain/

## Related Projects

- [CycloneDX](https://cyclonedx.org/) - SBOM standard format
- [cdxgen](https://github.com/CycloneDX/cdxgen) - SBOM generation tool
- [Syft](https://github.com/anchore/syft) - Container image analysis tool
- [Dependency-Track](https://dependencytrack.org/) - SBOM analysis platform

## Acknowledgments

This project uses the following open-source projects:

- [CycloneDX cdxgen](https://github.com/CycloneDX/cdxgen) - Apache 2.0
- [Anchore Syft](https://github.com/anchore/syft) - Apache 2.0
- [Aqua Security Trivy](https://github.com/aquasecurity/trivy) - Apache 2.0

---

Made by SK Telecom Open Source Program Office