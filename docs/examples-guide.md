# Examples Guide

This guide explains how to use the example projects in the `examples/` directory and how to create your own.

## Table of Contents

- [Overview](#overview)
- [Directory Structure](#directory-structure)
- [Using Examples](#using-examples)
- [Available Examples](#available-examples)
- [Creating New Examples](#creating-new-examples)
- [Best Practices](#best-practices)

## Overview

The `examples/` directory contains sample projects for each supported language ecosystem. These examples demonstrate:

- Minimal viable project structure
- Typical dependency configurations
- Expected SBOM output
- Usage patterns for SBOM Tools

## Directory Structure

```
examples/
├── java-maven/          # Java with Maven
│   ├── README.md
│   ├── pom.xml
│   └── src/
├── java-gradle/         # Java with Gradle
│   ├── README.md
│   ├── build.gradle
│   └── src/
├── nodejs/              # Node.js with npm
│   ├── README.md
│   ├── package.json
│   └── index.js
├── python/              # Python with pip
│   ├── README.md
│   ├── requirements.txt
│   └── app.py
├── ruby/                # Ruby with Bundler
│   ├── README.md
│   ├── Gemfile
│   └── app.rb
├── php/                 # PHP with Composer
│   ├── README.md
│   ├── composer.json
│   └── index.php
├── rust/                # Rust with Cargo
│   ├── README.md
│   ├── Cargo.toml
│   └── src/
├── go/                  # Go with modules
│   ├── README.md
│   ├── go.mod
│   └── main.go
├── dotnet/              # .NET with NuGet
│   ├── README.md
│   ├── *.csproj
│   └── Program.cs
└── docker/              # Docker image analysis
    ├── README.md
    └── Dockerfile
```

## Using Examples

### Quick Start

```bash
# Navigate to any example
cd examples/nodejs

# Generate SBOM
../../scripts/scan-sbom.sh --project "NodeExample" --version "1.0.0" --generate-only

# View results
cat NodeExample_1.0.0_bom.json | jq '.components | length'
cat NodeExample_1.0.0_bom.json | jq '.components[0]'
```

### Step-by-Step Process

1. Choose an example
   ```bash
   cd examples/python
   ```

2. Review the README
   ```bash
   cat README.md
   ```

3. Examine project structure
   ```bash
   ls -la
   cat requirements.txt
   ```

4. Generate SBOM
   ```bash
   ../../scripts/scan-sbom.sh \
     --project "PythonExample" \
     --version "1.0.0" \
     --generate-only
   ```

5. Analyze output
   ```bash
   # Count components
   jq '.components | length' PythonExample_1.0.0_bom.json
   
   # View component details
   jq '.components[] | {name, version, licenses}' PythonExample_1.0.0_bom.json
   
   # Check for specific package
   jq '.components[] | select(.name == "flask")' PythonExample_1.0.0_bom.json
   ```

### Using Different Scan Modes

#### Source Code (Default)
```bash
cd examples/nodejs
../../scripts/scan-sbom.sh --project "App" --version "1.0" --generate-only
```

#### Docker Image
```bash
cd examples/docker
# Build image first
docker build -t myapp:1.0 .

# Scan image
../../scripts/scan-sbom.sh \
  --project "MyApp" \
  --version "1.0" \
  --target "myapp:1.0" \
  --generate-only
```

## Available Examples

### Java Maven

Location: `examples/java-maven/`

Description: Spring Boot REST API with common dependencies

Dependencies:
- spring-boot-starter-web
- Transitive dependencies (~50 components)

Usage:
```bash
cd examples/java-maven
../../scripts/scan-sbom.sh --project "JavaMaven" --version "1.0.0" --generate-only
```

Expected Output:
- Components: ~50-60
- Includes Spring Framework, Tomcat, Jackson, etc.

---

### Java Gradle

Location: `examples/java-gradle/`

Description: Gradle-based Java application

Dependencies:
- guava
- junit (test scope)

Usage:
```bash
cd examples/java-gradle
../../scripts/scan-sbom.sh --project "JavaGradle" --version "1.0.0" --generate-only
```

Expected Output:
- Components: ~20-30
- Includes Guava and its dependencies

---

### Node.js

Location: `examples/nodejs/`

Description: Express web server

Dependencies:
- express
- dotenv

Usage:
```bash
cd examples/nodejs
../../scripts/scan-sbom.sh --project "NodeApp" --version "1.0.0" --generate-only
```

Expected Output:
- Components: ~60-70
- Includes Express, body-parser, cookie-parser, etc.

---

### Python

Location: `examples/python/`

Description: Flask REST API

Dependencies:
- flask
- requests
- python-dotenv

Usage:
```bash
cd examples/python
../../scripts/scan-sbom.sh --project "PythonApp" --version "1.0.0" --generate-only
```

Expected Output:
- Components: ~15-20
- Includes Flask, Werkzeug, Jinja2, etc.

---

### Ruby

Location: `examples/ruby/`

Description: Sinatra web application

Dependencies:
- sinatra
- rack

Usage:
```bash
cd examples/ruby
../../scripts/scan-sbom.sh --project "RubyApp" --version "1.0.0" --generate-only
```

Expected Output:
- Components: ~5-10
- Includes Sinatra, Rack, Mustermann

---

### PHP

Location: `examples/php/`

Description: Slim framework API

Dependencies:
- slim/slim
- psr/log

Usage:
```bash
cd examples/php
../../scripts/scan-sbom.sh --project "PHPApp" --version "1.0.0" --generate-only
```

Expected Output:
- Components: ~8-12
- Includes Slim, PSR interfaces, Pimple

---

### Rust

Location: `examples/rust/`

Description: Actix-web HTTP server

Dependencies:
- actix-web
- serde

Usage:
```bash
cd examples/rust
../../scripts/scan-sbom.sh --project "RustApp" --version "1.0.0" --generate-only
```

Expected Output:
- Components: ~30-40
- Includes actix-web, tokio, serde, etc.

---

### Go

Location: `examples/go/`

Description: Gin web framework

Dependencies:
- github.com/gin-gonic/gin
- github.com/spf13/cobra

Usage:
```bash
cd examples/go
../../scripts/scan-sbom.sh --project "GoApp" --version "1.0.0" --generate-only
```

Expected Output:
- Components: ~30-40
- Includes Gin, Cobra, and their dependencies

---

### .NET

Location: `examples/dotnet/`

Description: ASP.NET Core web API

Dependencies:
- Microsoft.AspNetCore.App
- Newtonsoft.Json

Usage:
```bash
cd examples/dotnet
../../scripts/scan-sbom.sh --project "DotNetApp" --version "1.0.0" --generate-only
```

Expected Output:
- Components: ~40-50
- Includes ASP.NET Core packages

---

### Docker

Location: `examples/docker/`

Description: Multi-stage Docker build

Usage:
```bash
cd examples/docker
# Build image
docker build -t example-app:1.0 .

# Scan image
../../scripts/scan-sbom.sh \
  --project "DockerExample" \
  --version "1.0" \
  --target "example-app:1.0" \
  --generate-only
```

Expected Output:
- Components: ~100+
- Includes OS packages, runtime libraries

## Creating New Examples

### Template Structure

```
examples/your-language/
├── README.md           # Documentation
├── [manifest-file]     # Dependency manifest
└── [source-files]      # Minimal working code
```

### Example README Template

```markdown
# [Language] Example

This example demonstrates SBOM generation for [Language] projects using [Package Manager].

## Project Structure

- `[manifest]`: Defines project dependencies
- `[source]`: Minimal [language] application
- `[config]`: Optional configuration

## Dependencies

- [package-1] ([version]): [description]
- [package-2] ([version]): [description]

## Generate SBOM

```bash
cd examples/your-language
../../scripts/scan-sbom.sh --project "YourApp" --version "1.0.0" --generate-only
```

## Expected Output

The scan generates `YourApp_1.0.0_bom.json` containing:
- X direct dependencies
- Y total components (including transitive)
- License information for each component

### Sample Components

- [package-1] v[version]
- [package-2] v[version]
- ...

## Validate Results

```bash
# Count components
jq '.components | length' YourApp_1.0.0_bom.json

# View specific package
jq '.components[] | select(.name == "[package]")' YourApp_1.0.0_bom.json
```

## Common Issues

### Issue 1: [Common Problem]

Error: [Error message]

Solution: [How to fix]

## Next Steps

- Modify dependencies in `[manifest]`
- Add more packages to test
- Compare SBOM output with different versions
```

### Minimal Project Requirements

Each example should:

1. Be minimal - Only essential code
2. Have dependencies - At least 2-3 packages
3. Be working - Code should compile/run
4. Be documented - Clear README
5. Be tested - Included in test suite

### Example Checklist

- [ ] README.md with usage instructions
- [ ] Manifest file with dependencies
- [ ] Minimal source code
- [ ] Works with scan-sbom.sh
- [ ] Generates non-empty SBOM
- [ ] Test case in tests/test-scan.sh
- [ ] Documented in this guide

### Naming Conventions

Directory names:
- Lowercase
- Hyphen-separated
- Language or framework name
- Example: `java-maven`, `nodejs`, `python-flask`

File names:
- Standard for the ecosystem
- `pom.xml`, `package.json`, `requirements.txt`, etc.
- No custom naming

Project names in examples:
- PascalCase
- Descriptive
- Example: `JavaMavenExample`, `NodeExpressApp`

## Best Practices

### 1. Keep It Simple

```
Good Example:
- 3-5 dependencies
- Single source file
- Minimal configuration

Bad Example:
- 50+ dependencies
- Multiple modules
- Complex build setup
```

### 2. Use Popular Packages

```
Good:
- express (Node.js)
- flask (Python)
- spring-boot (Java)

Avoid:
- Obscure packages
- Deprecated libraries
- Beta versions
```

### 3. Document Expected Output

```markdown
## Expected Components

After running the scan, you should see approximately:
- 42 total components
- Including: express, body-parser, cookie-parser
- All with MIT or Apache-2.0 licenses
```

### 4. Include Version Information

```json
// package.json
{
  "dependencies": {
    "express": "^4.18.2",  // Specific version
    "dotenv": "^16.0.3"
  }
}
```

### 5. Add Troubleshooting

```markdown
## Troubleshooting

### Dependencies not found
If scan shows 0 components:
1. Check internet connection
2. Verify package registry access
3. Review entrypoint.sh logs
```

## Testing Examples

### Manual Testing

```bash
# Test each example
for dir in examples/*/; do
  cd "$dir"
  name=$(basename "$dir")
  ../../scripts/scan-sbom.sh --project "$name" --version "1.0" --generate-only
  cd ../..
done
```

### Automated Testing

Example test case template:

```bash
# Test in tests/test-scan.sh
cd examples/your-language
if "$SCAN_SCRIPT" --project "Test" --version "1.0" --generate-only; then
  if [ -f "Test_1.0_bom.json" ]; then
    COMP=$(jq '.components | length' Test_1.0_bom.json)
    if [ "$COMP" -gt 0 ]; then
      print_success "Example test passed ($COMP components)"
    fi
  fi
fi
```

## Common Patterns

### Python with Virtual Environment

```bash
# In example directory
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate

# Then scan
../../scripts/scan-sbom.sh --project "App" --version "1.0" --generate-only
```

### Node.js with Package Lock

```bash
# Generate package-lock.json first
npm install

# Then scan
../../scripts/scan-sbom.sh --project "App" --version "1.0" --generate-only
```

### Java with Dependency Download

```bash
# Download dependencies first
mvn dependency:resolve

# Then scan
../../scripts/scan-sbom.sh --project "App" --version "1.0" --generate-only
```

## Validation

### Validate SBOM Output

```bash
# Check structure
jq '.' YourApp_1.0.0_bom.json > /dev/null && echo "Valid JSON"

# Check CycloneDX compliance
jq '.bomFormat == "CycloneDX"' YourApp_1.0.0_bom.json

# Check components exist
jq '.components | length > 0' YourApp_1.0.0_bom.json

# Check for required fields
jq '.components[0] | has("name") and has("version")' YourApp_1.0.0_bom.json
```

### Component Verification

```bash
# List all component names
jq -r '.components[].name' YourApp_1.0.0_bom.json | sort

# Find specific component
jq '.components[] | select(.name == "express")' YourApp_1.0.0_bom.json

# Check licenses
jq -r '.components[] | "\(.name): \(.licenses[0].license.id // "Unknown")"' YourApp_1.0.0_bom.json
```

## Troubleshooting

### No Components in SBOM

Cause: Dependencies not downloaded

Solution:
```bash
# Manually install dependencies first
npm install        # Node.js
pip install -r requirements.txt  # Python
mvn install       # Java Maven
```

### Wrong Component Count

Cause: Cached dependencies or version mismatch

Solution:
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install

# Or for Maven
mvn clean dependency:purge-local-repository
```

### Scan Fails

Cause: Missing manifest files

Solution:
```bash
# Verify files exist
ls -la package.json  # Node.js
ls -la pom.xml      # Java
ls -la requirements.txt  # Python
```

## Contributing Examples

To contribute a new example:

1. Create directory in `examples/`
2. Add manifest and source files
3. Create detailed README.md
4. Test SBOM generation
5. Add test case to test-scan.sh
6. Update this guide
7. Submit pull request

See [CONTRIBUTING.md](../CONTRIBUTING.md) for details.

## References

- [CycloneDX BOM Examples](https://github.com/CycloneDX/bom-examples)
- [cdxgen Examples](https://github.com/CycloneDX/cdxgen/tree/master/test)
- Package manager documentation for each language

## Getting Help

If you have questions:
- Check example README files
- Review [ARCHITECTURE.md](../ARCHITECTURE.md)
- See [TESTING_GUIDE.md](../TESTING_GUIDE.md)
- Open an issue on GitHub
