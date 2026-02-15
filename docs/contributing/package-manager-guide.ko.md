# Package Manager Integration Guide

This guide explains how to add support for new package managers to SBOM Tools.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Step-by-Step Guide](#step-by-step-guide)
- [Example: Adding Go Modules](#example-adding-go-modules)
- [Example: Adding Swift Package Manager](#example-adding-swift-package-manager)
- [Testing Your Integration](#testing-your-integration)
- [Best Practices](#best-practices)

## Overview

SBOM Tools supports multiple package managers through a modular architecture. Adding support for a new package manager typically involves:

1. Installing the runtime/toolchain in the Docker image
2. Adding dependency resolution logic in `entrypoint.sh`
3. Testing with example projects
4. Updating documentation

## Prerequisites

Before adding a new package manager, ensure you have:

- [ ] Docker installed locally
- [ ] Basic understanding of the package manager
- [ ] Access to the sbom-tools repository
- [ ] Knowledge of Bash scripting

## Step-by-Step Guide

### Step 1: Update the Dockerfile

Add the package manager's runtime and tools to `docker/Dockerfile`.

**Location:** After existing language runtimes

```dockerfile
# Example: Adding Go support
RUN apt-get update && apt-get install -y --no-install-recommends \
    golang-go \
    && rm -rf /var/lib/apt/lists/*

# Set Go environment variables
ENV GOPATH="/root/go"
ENV PATH="$PATH:/usr/local/go/bin:$GOPATH/bin"
```

**Best practices:**
- Use `--no-install-recommends` to minimize image size
- Clean up apt cache with `rm -rf /var/lib/apt/lists/*`
- Install specific versions for reproducibility when possible
- Set necessary environment variables

### Step 2: Add Dependency Resolution in entrypoint.sh

Add logic to detect and resolve dependencies for the new package manager.

**Location:** In the `SOURCE` mode section, after existing package managers

```bash
# Handle [Package Manager Name]
if [ -f "[manifest-file]" ] && command -v [tool] >/dev/null 2>&1; then
    echo "[INFO] Found [manifest-file]. Installing dependencies..."
    [dependency-install-command] 2>&1 | grep -i error || true
fi
```

**Template:**

```bash
# Handle [Package Manager]
if [ -f "[lock-file-or-manifest]" ] && command -v [cli-tool] >/dev/null 2>&1; then
    echo "[INFO] Found [lock-file-or-manifest]. Processing dependencies..."
    
    # Optional: Generate lock file if it doesn't exist
    if [ ! -f "[lock-file]" ]; then
        echo "[INFO] Generating lock file..."
        [generate-lock-command] 2>/dev/null || true
    fi
    
    # Download/resolve dependencies
    echo "[INFO] Downloading dependencies..."
    if [dependency-download-command] 2>&1 | tee /tmp/[pm].log | tail -10; then
        echo "[INFO] Dependencies resolved successfully"
    else
        echo "[WARN] Some dependencies may not be available"
    fi
    
    # Optional: Count downloaded packages
    if [ -d "[cache-directory]" ]; then
        PKG_COUNT=$(find [cache-directory] -type f -name "[pattern]" 2>/dev/null | wc -l)
        echo "[INFO] Downloaded packages: $PKG_COUNT"
    fi
fi
```

### Step 3: Update Documentation

Update relevant documentation files to mention the new package manager.

**Files to update:**

1. **README.md** - Add to supported languages table
2. **README.ko.md** - Korean translation
3. **docs/usage-guide.md** - Add usage example
4. **ARCHITECTURE.md** - Update component diagram

**Example README.md update:**

```markdown
| Language | Package Managers | Manifest Files |
|----------|------------------|----------------|
| Go | Go modules | go.mod, go.sum |
```

### Step 4: Create Example Project

Add an example project in `examples/[language-name]/`.

**Structure:**

```
examples/your-language/
├── README.md           # How to use this example
├── [manifest-file]     # Package manifest
└── [source-files]      # Minimal source code
```

**Example README.md:**

```markdown
# [Language Name] Example

This example demonstrates SBOM generation for [Language] projects.

## Project Structure

- `[manifest-file]`: Defines project dependencies
- `[source-file]`: Minimal application code

## Generate SBOM

```bash
cd examples/your-language
../../scripts/scan-sbom.sh --project "YourApp" --version "1.0.0" --generate-only
```

## Expected Output

The scan will generate `YourApp_1.0.0_bom.json` containing:
- Direct dependencies
- Transitive dependencies
- License information
```

### Step 5: Add Test Case

Add a test case to `tests/test-scan.sh`.

**Location:** After existing test cases

**Template:**

```bash
# ========================================================
# Test N: [Language] project
# ========================================================
print_test "Test N/10: [Language] project"

mkdir -p [language]-project
cd [language]-project

# Create minimal project
cat > [manifest-file] <<'EOF'
[manifest-content]
EOF

# Optional: Create source file
cat > [source-file] <<'EOF'
[minimal-source-code]
EOF

# Run scan
if "$SCAN_SCRIPT" --project "Test[Language]" --version "1.0.0" --generate-only > /dev/null 2>&1; then
    if FOUND=$(find_bom_file "Test[Language]" "1.0.0"); then
        COMP_COUNT=$(cat "$FOUND" | jq '.components | length' 2>/dev/null || echo "0")
        if [ "$COMP_COUNT" -gt 0 ]; then
            print_success "[Language] project ($COMP_COUNT components)"
            ((PASSED++))
        else
            print_error "[Language] project (SBOM empty)"
            ((FAILED++))
        fi
    else
        print_error "[Language] project (SBOM not generated)"
        ((FAILED++))
    fi
else
    print_error "[Language] project (Scan failed)"
    ((FAILED++))
fi

cd "$TEST_DIR"
```

## Example: Adding Go Modules

Here's a complete example of adding Go modules support.

### 1. Dockerfile

```dockerfile
# Go language support
RUN wget -q https://go.dev/dl/go1.21.5.linux-amd64.tar.gz \
    && tar -C /usr/local -xzf go1.21.5.linux-amd64.tar.gz \
    && rm go1.21.5.linux-amd64.tar.gz

ENV PATH="/usr/local/go/bin:${PATH}"
ENV GOPATH="/root/go"
```

### 2. entrypoint.sh

```bash
# Handle Go modules
if [ -f "go.mod" ] && command -v go >/dev/null 2>&1; then
    echo "[INFO] Found go.mod. Processing Go modules..."
    
    # Download dependencies
    echo "[INFO] Downloading Go modules..."
    if go mod download 2>&1 | tee /tmp/go.log | tail -10; then
        echo "[INFO] Go modules downloaded successfully"
    else
        echo "[WARN] Some modules may not be available"
    fi
    
    # Verify dependencies
    go mod verify 2>/dev/null || true
    
    # Count modules
    if [ -d "$GOPATH/pkg/mod" ]; then
        MOD_COUNT=$(find "$GOPATH/pkg/mod" -type d -mindepth 1 -maxdepth 1 2>/dev/null | wc -l)
        echo "[INFO] Downloaded modules: $MOD_COUNT"
    fi
fi
```

### 3. Example Project (examples/go/)

**go.mod:**
```go
module example.com/hello

go 1.21

require (
    github.com/gin-gonic/gin v1.9.1
    github.com/spf13/cobra v1.8.0
)
```

**main.go:**
```go
package main

import (
    "fmt"
    "github.com/gin-gonic/gin"
)

func main() {
    r := gin.Default()
    r.GET("/", func(c *gin.Context) {
        c.JSON(200, gin.H{"message": "Hello World"})
    })
    fmt.Println("Server starting...")
}
```

**README.md:**
```markdown
# Go Example

Demonstrates SBOM generation for Go projects using Go modules.

## Generate SBOM

```bash
cd examples/go
../../scripts/scan-sbom.sh --project "GoApp" --version "1.0.0" --generate-only
```

## Expected Components

- gin-gonic/gin
- spf13/cobra
- And their transitive dependencies (~30-40 components)
```

### 4. Test Case

```bash
# ========================================================
# Test 11: Go modules project
# ========================================================
print_test "Test 11: Go modules project"

mkdir -p go-project
cd go-project

cat > go.mod <<'EOF'
module example.com/test

go 1.21

require github.com/gin-gonic/gin v1.9.1
EOF

cat > main.go <<'EOF'
package main
import "fmt"
func main() { fmt.Println("Hello") }
EOF

if "$SCAN_SCRIPT" --project "TestGo" --version "1.0.0" --generate-only > /dev/null 2>&1; then
    if FOUND=$(find_bom_file "TestGo" "1.0.0"); then
        COMP_COUNT=$(cat "$FOUND" | jq '.components | length')
        if [ "$COMP_COUNT" -gt 0 ]; then
            print_success "Go project ($COMP_COUNT components)"
            ((PASSED++))
        else
            print_error "Go project (SBOM empty)"
            ((FAILED++))
        fi
    fi
fi

cd "$TEST_DIR"
```

## Example: Adding Swift Package Manager

### 1. Dockerfile

```dockerfile
# Swift support
RUN apt-get update && apt-get install -y --no-install-recommends \
    binutils \
    git \
    libc6-dev \
    libcurl4-openssl-dev \
    libedit2 \
    libgcc-11-dev \
    libpython3.11 \
    libsqlite3-0 \
    libstdc++-11-dev \
    libxml2-dev \
    libz3-dev \
    pkg-config \
    tzdata \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Swift
RUN wget -q https://download.swift.org/swift-5.9.2-release/ubuntu2204/swift-5.9.2-RELEASE/swift-5.9.2-RELEASE-ubuntu22.04.tar.gz \
    && tar xzf swift-5.9.2-RELEASE-ubuntu22.04.tar.gz \
    && mv swift-5.9.2-RELEASE-ubuntu22.04 /usr/share/swift \
    && rm swift-5.9.2-RELEASE-ubuntu22.04.tar.gz

ENV PATH="/usr/share/swift/usr/bin:${PATH}"
```

### 2. entrypoint.sh

```bash
# Handle Swift Package Manager
if [ -f "Package.swift" ] && command -v swift >/dev/null 2>&1; then
    echo "[INFO] Found Package.swift. Processing Swift packages..."
    
    # Resolve dependencies
    echo "[INFO] Resolving Swift packages..."
    if swift package resolve 2>&1 | tee /tmp/swift.log | tail -10; then
        echo "[INFO] Swift packages resolved successfully"
    else
        echo "[WARN] Some packages may not be available"
    fi
    
    # Show dependency tree
    swift package show-dependencies --format json > /tmp/swift-deps.json 2>/dev/null || true
fi
```

## Testing Your Integration

### Local Testing

```bash
# 1. Build Docker image
cd docker
docker build -t sbom-scanner:test .

# 2. Test with example project
cd ../examples/your-language
SBOM_SCANNER_IMAGE=sbom-scanner:test \
  ../../scripts/scan-sbom.sh --project "Test" --version "1.0" --generate-only

# 3. Verify SBOM
cat Test_1.0_bom.json | jq '.components | length'
cat Test_1.0_bom.json | jq '.components[0]'
```

### Integration Testing

```bash
# Run full test suite
SBOM_SCANNER_IMAGE=sbom-scanner:test ./tests/test-scan.sh
```

### Validation Checklist

- [ ] Dependencies are downloaded correctly
- [ ] SBOM file is generated
- [ ] Components count > 0
- [ ] License information is included
- [ ] No errors in logs (warnings are OK)
- [ ] Works with minimal project
- [ ] Works with complex project

## Best Practices

### 1. Error Handling

Always handle errors gracefully:

```bash
# Good
if command 2>&1 | tee /tmp/log.txt; then
    echo "[INFO] Success"
else
    echo "[WARN] Failed but continuing..."
fi

# Avoid failing the entire scan
command || true
```

### 2. Logging

Provide clear, actionable logs:

```bash
echo "[INFO] Found package.json. Installing dependencies..."
echo "[INFO] Downloaded 42 packages"
echo "[WARN] 3 packages had warnings (non-critical)"
echo "[ERROR] Failed to download package X"
```

### 3. Performance

Optimize for speed:

```bash
# Use quiet/silent mode for package managers
npm install --quiet
pip install --quiet

# Only show summary
command 2>&1 | tail -10
```

### 4. Caching

Support cache mounts for faster subsequent runs:

```bash
# In scan-sbom.sh, add cache mount
if [ -d "$HOME/.your-cache" ]; then
    CACHE_MOUNTS="$CACHE_MOUNTS -v \"$HOME/.your-cache\":/root/.your-cache"
fi
```

### 5. Documentation

Always update:
- README.md (supported languages)
- Usage guide (examples)
- Architecture diagram
- Test suite

## Troubleshooting

### Common Issues

**Issue 1: Package manager not found**
```
Error: command not found
```
**Solution:** Ensure tool is installed in Dockerfile and in PATH

**Issue 2: Dependencies not resolved**
```
SBOM is empty
```
**Solution:** Check if dependency download actually runs, verify lock file generation

**Issue 3: Permissions**
```
Permission denied
```
**Solution:** Ensure files are readable, use appropriate user permissions

**Issue 4: Network issues**
```
Failed to download
```
**Solution:** Check network connectivity, verify package repository URLs

## Pull Request Checklist

Before submitting your integration:

- [ ] Dockerfile updated with runtime
- [ ] entrypoint.sh includes dependency logic
- [ ] Example project created and documented
- [ ] Test case added to test-scan.sh
- [ ] All tests pass locally
- [ ] Documentation updated (README, usage-guide)
- [ ] ARCHITECTURE.md updated
- [ ] Code follows existing style
- [ ] Commit messages are clear

## Getting Help

If you encounter issues:

1. Check existing integrations for reference
2. Search issues on GitHub
3. Ask in discussions
4. Contact maintainers

## Examples in the Wild

Learn from existing integrations:

- **Python**: `pip` with `requirements.txt`
- **Node.js**: `npm` with `package.json`
- **Java**: `mvn` with `pom.xml`
- **Ruby**: `bundle` with `Gemfile`
- **PHP**: `composer` with `composer.json`
- **Rust**: `cargo` with `Cargo.toml`

## References

- [cdxgen Supported Languages](https://github.com/CycloneDX/cdxgen#supported-languages)
- [CycloneDX Specification](https://cyclonedx.org/specification/overview/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for general contribution guidelines.
