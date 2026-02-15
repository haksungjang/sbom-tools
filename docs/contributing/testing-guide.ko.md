# Testing Guide

This guide covers testing strategies, frameworks, and procedures for SBOM Tools.

## Table of Contents

- [Overview](#overview)
- [Test Structure](#test-structure)
- [Running Tests](#running-tests)
- [Adding New Tests](#adding-new-tests)
- [Test Framework Details](#test-framework-details)
- [CI/CD Integration](#cicd-integration)
- [Troubleshooting](#troubleshooting)

## Overview

SBOM Tools uses a comprehensive testing strategy:

```
┌─────────────────────────────────────┐
│     Integration Tests               │
│  (tests/test-scan.sh)              │
│                                     │
│  ┌────────────┐  ┌──────────────┐  │
│  │  Language  │  │  Scan Mode   │  │
│  │   Tests    │  │    Tests     │  │
│  └────────────┘  └──────────────┘  │
│                                     │
│  ┌────────────┐  ┌──────────────┐  │
│  │  Example   │  │    Error     │  │
│  │   Tests    │  │   Handling   │  │
│  └────────────┘  └──────────────┘  │
└─────────────────────────────────────┘
           │
           ▼
    ┌─────────────────┐
    │   CI/CD Tests   │
    │ (GitHub Actions)│
    └─────────────────┘
```

### Test Categories

1. **Language Tests** - Verify SBOM generation for each supported language
2. **Mode Tests** - Test SOURCE, IMAGE, BINARY, ROOTFS modes
3. **Example Tests** - Validate all example projects
4. **Integration Tests** - End-to-end workflow validation

## Test Structure

### Directory Layout

```
tests/
├── test-scan.sh           # Main test suite
├── fixtures/              # Test data (future)
└── helpers/               # Test utilities (future)
```

### test-scan.sh Structure

```bash
#!/bin/bash

# Configuration
SCRIPT_DIR=...
TEST_DIR=...

# Helper Functions
print_header()  - Display section headers
print_test()    - Display test names
print_success() - Green checkmarks
print_error()   - Red X marks
find_bom_file() - Locate generated SBOM files

# Prerequisite Checks
- Docker installed
- Docker running
- scan-sbom.sh exists

# Test Cases
Test 1/10: Node.js project
Test 2/10: Python project
Test 3/10: Java Maven project
...
Test 10/10: Example validation

# Summary
- Total tests
- Passed count
- Failed count
- Success rate

# Cleanup
- Remove test workspace
```

## Running Tests

### Full Test Suite

```bash
# From project root
./tests/test-scan.sh
```

**Expected Output:**
```
==========================================
 SBOM Tools - Integration Test
 Version: 1.0.0
==========================================

[INFO] Checking prerequisites...
[✓] Docker check passed
[✓] Scan script check passed

[INFO] Starting tests...

[TEST] Test 1/10: Node.js project (npm)
[✓] Node.js project (69 components)
[TEST] Test 2/10: Python project (pip)
[✓] Python project (18 components)
...

==========================================
 Test Summary
==========================================

Total tests: 10
Passed: 10
Failed: 0
Success rate: 100.0%
```

### Specific Test

To run a specific test, modify `test-scan.sh` temporarily:

```bash
# Comment out other tests
# Test 1/10: Node.js project
# ...

# Keep only the test you want
Test 3/10: Java Maven project
```

### With Custom Image

```bash
# Build local image
docker build -t sbom-scanner:test ./docker

# Test with it
SBOM_SCANNER_IMAGE=sbom-scanner:test ./tests/test-scan.sh
```

### Debug Mode

```bash
# Show all output (remove > /dev/null redirects)
# Edit test-scan.sh and change:
"$SCAN_SCRIPT" ... > /dev/null 2>&1
# To:
"$SCAN_SCRIPT" ... 2>&1 | tee test-output.log
```

## Adding New Tests

### Template

```bash
# ========================================================
# Test N/M: [Description]
# ========================================================
print_test "Test N/M: [Description]"

# Create test directory
mkdir -p test-project
cd test-project

# Create project files
cat > manifest.file <<'EOF'
[content]
EOF

# Run scan
if "$SCAN_SCRIPT" --project "TestName" --version "1.0.0" --generate-only > /dev/null 2>&1; then
    # Find SBOM file
    if FOUND=$(find_bom_file "TestName" "1.0.0"); then
        # Validate SBOM
        COMP_COUNT=$(cat "$FOUND" | jq '.components | length' 2>/dev/null || echo "0")
        
        if [ "$COMP_COUNT" -gt 0 ]; then
            print_success "[Description] ($COMP_COUNT components)"
            ((PASSED++))
        else
            print_error "[Description] (SBOM empty)"
            ((FAILED++))
        fi
    else
        print_error "[Description] (SBOM not generated)"
        ((FAILED++))
    fi
else
    print_error "[Description] (Scan failed)"
    ((FAILED++))
fi

cd "$TEST_DIR"
```

### Example: Adding Go Test

```bash
# ========================================================
# Test 11/15: Go modules project
# ========================================================
print_test "Test 11/15: Go modules project"

mkdir -p go-project
cd go-project

cat > go.mod <<'EOF'
module example.com/test

go 1.21

require (
    github.com/gin-gonic/gin v1.9.1
)
EOF

cat > main.go <<'EOF'
package main

import (
    "github.com/gin-gonic/gin"
)

func main() {
    r := gin.Default()
    r.Run()
}
EOF

if "$SCAN_SCRIPT" --project "TestGo" --version "1.0.0" --generate-only > /dev/null 2>&1; then
    if FOUND=$(find_bom_file "TestGo" "1.0.0"); then
        COMP_COUNT=$(cat "$FOUND" | jq '.components | length' 2>/dev/null || echo "0")
        
        # Go projects typically have 30+ components
        if [ "$COMP_COUNT" -gt 20 ]; then
            print_success "Go project ($COMP_COUNT components)"
            ((PASSED++))
        else
            print_error "Go project (Too few components: $COMP_COUNT)"
            ((FAILED++))
        fi
    else
        print_error "Go project (SBOM not generated)"
        ((FAILED++))
    fi
else
    print_error "Go project (Scan failed)"
    ((FAILED++))
fi

cd "$TEST_DIR"
```

### Test Validation Criteria

Each test should validate:

1. **Scan execution** - Command returns 0
2. **SBOM file existence** - File is created
3. **SBOM content** - Components array is not empty
4. **Component count** - Reasonable number for the project
5. **SBOM format** - Valid JSON/CycloneDX

### Advanced Validation

```bash
# Validate SBOM structure
validate_sbom() {
    local file=$1
    
    # Check bomFormat
    if ! cat "$file" | jq -e '.bomFormat == "CycloneDX"' > /dev/null 2>&1; then
        echo "Invalid bomFormat"
        return 1
    fi
    
    # Check specVersion
    if ! cat "$file" | jq -e '.specVersion' > /dev/null 2>&1; then
        echo "Missing specVersion"
        return 1
    fi
    
    # Check components
    if ! cat "$file" | jq -e '.components | type == "array"' > /dev/null 2>&1; then
        echo "Invalid components"
        return 1
    fi
    
    return 0
}

# Use in test
if validate_sbom "$FOUND"; then
    print_success "SBOM validation passed"
else
    print_error "SBOM validation failed"
fi
```

## Test Framework Details

### Helper Functions

#### print_header

```bash
print_header() {
    echo "=========================================="
    echo " $1"
    echo "=========================================="
}
```

**Usage:**
```bash
print_header "Starting Integration Tests"
```

#### print_test

```bash
print_test() {
    echo "[TEST] $1"
}
```

**Usage:**
```bash
print_test "Test 1/10: Node.js project"
```

#### print_success

```bash
print_success() {
    echo "[✓] $1"
}
```

**Usage:**
```bash
print_success "Test passed (42 components)"
```

#### print_error

```bash
print_error() {
    echo "[✗] $1"
}
```

**Usage:**
```bash
print_error "Test failed (SBOM empty)"
```

#### find_bom_file

```bash
find_bom_file() {
    local project=$1
    local version=$2
    local safe_project=$(echo "$project" | sed 's/[^a-zA-Z0-9.-]/_/g')
    local safe_version=$(echo "$version" | sed 's/[^a-zA-Z0-9.-]/_/g')
    local filename="${safe_project}_${safe_version}_bom.json"
    
    if [ -f "$filename" ]; then
        echo "$filename"
        return 0
    fi
    return 1
}
```

**Usage:**
```bash
if FOUND=$(find_bom_file "MyProject" "1.0.0"); then
    echo "Found: $FOUND"
fi
```

### Test Counters

```bash
# Initialize
TOTAL=0
PASSED=0
FAILED=0

# Increment
((TOTAL++))
((PASSED++))
((FAILED++))

# Calculate
SUCCESS_RATE=$(awk "BEGIN {printf \"%.1f\", ($PASSED/$TOTAL)*100}")
```

### Prerequisites Check

```bash
# Docker availability
if ! command -v docker &> /dev/null; then
    print_error "Docker not installed"
    exit 1
fi

# Docker daemon
if ! docker info > /dev/null 2>&1; then
    print_error "Docker daemon not running"
    exit 1
fi

# Script existence
if [ ! -f "$SCAN_SCRIPT" ]; then
    print_error "scan-sbom.sh not found"
    exit 1
fi
```

## CI/CD Integration

### GitHub Actions Workflow

**.github/workflows/test.yml:**

```yaml
name: Integration Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Docker
      uses: docker/setup-buildx-action@v3
    
    - name: Build Docker image
      run: |
        cd docker
        docker build -t sbom-scanner:test .
    
    - name: Run integration tests
      env:
        SBOM_SCANNER_IMAGE: sbom-scanner:test
      run: |
        chmod +x tests/test-scan.sh
        ./tests/test-scan.sh
    
    - name: Upload test results
      if: always()
      uses: actions/upload-artifact@v4
      with:
        name: test-results
        path: tests/test-workspace/
```

### Test Matrix

For testing across multiple platforms:

```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest]
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Run tests
      run: ./tests/test-scan.sh
```

### Performance Testing

```yaml
- name: Measure performance
  run: |
    time ./tests/test-scan.sh
    
- name: Check test duration
  run: |
    # Fail if tests take > 10 minutes
    timeout 600 ./tests/test-scan.sh
```

## Troubleshooting

### Common Issues

#### Issue 1: Docker Not Running

**Error:**
```
[ERROR] Docker daemon is not running
```

**Solution:**
```bash
# Start Docker
sudo systemctl start docker

# Or on macOS
open -a Docker
```

#### Issue 2: Permission Denied

**Error:**
```
[ERROR] Permission denied: scan-sbom.sh
```

**Solution:**
```bash
chmod +x scripts/scan-sbom.sh
chmod +x tests/test-scan.sh
```

#### Issue 3: SBOM Not Generated

**Error:**
```
[✗] Test failed (SBOM not generated)
```

**Debug:**
```bash
# Run scan manually with output
cd tests/test-workspace/test-project
../../../scripts/scan-sbom.sh --project Test --version 1.0 --generate-only

# Check for errors in output
```

#### Issue 4: Empty SBOM

**Error:**
```
[✗] Test failed (SBOM empty)
```

**Debug:**
```bash
# Check SBOM content
cat Test_1.0_bom.json | jq .

# Verify dependencies were downloaded
# (Check entrypoint.sh logs)
```

#### Issue 5: jq Not Found

**Error:**
```
jq: command not found
```

**Solution:**
```bash
# Install jq
sudo apt-get install jq  # Debian/Ubuntu
brew install jq          # macOS
```

### Debug Checklist

- [ ] Docker is running
- [ ] Scripts are executable
- [ ] Test workspace is clean
- [ ] Docker image is built
- [ ] jq is installed
- [ ] Internet connection available (for dependencies)

### Verbose Mode

```bash
# Add at top of test-scan.sh
set -x  # Print commands before execution

# Or run with bash -x
bash -x tests/test-scan.sh
```

### Test Isolation

Each test should:
- Use separate directory
- Clean up after itself
- Not depend on other tests
- Be repeatable

```bash
# Good practice
mkdir -p unique-test-dir
cd unique-test-dir
# ... test logic ...
cd "$TEST_DIR"
# Cleanup happens in trap

# Bad practice
cd /tmp/test  # Shared directory
# ... test logic ...
# No cleanup
```

## Best Practices

### 1. Test Independence

Each test should run independently:

```bash
# Good
Test 1: Setup → Execute → Validate → Cleanup
Test 2: Setup → Execute → Validate → Cleanup

# Bad
Test 1: Setup → Execute
Test 2: Validate Test 1 → Execute
```

### 2. Clear Assertions

```bash
# Good
if [ "$COMP_COUNT" -gt 0 ]; then
    print_success "Has components ($COMP_COUNT)"
fi

# Bad
if [ "$COMP_COUNT" ]; then
    print_success "OK"
fi
```

### 3. Meaningful Messages

```bash
# Good
print_error "Maven test failed: SBOM empty (expected 50+ components)"

# Bad
print_error "Failed"
```

### 4. Cleanup

```bash
# Always use trap for cleanup
trap cleanup EXIT

cleanup() {
    if [ -d "$TEST_DIR" ]; then
        rm -rf "$TEST_DIR"
    fi
}
```

### 5. Timeouts

```bash
# Prevent hanging tests
timeout 60 "$SCAN_SCRIPT" ... || print_error "Timeout"
```

## Coverage Metrics

### Current Coverage

| Category | Tests | Coverage |
|----------|-------|----------|
| Languages | 9/9 | 100% |
| Scan Modes | 4/4 | 100% |
| Examples | 4/4 | 100% |
| Error Cases | 2/10 | 20% |

### Coverage Goals

- [ ] All supported languages
- [ ] All scan modes
- [ ] All example projects
- [ ] Error handling scenarios
- [ ] Edge cases (empty projects, large projects, etc.)

## Future Enhancements

1. **Unit Tests**
   - Test individual functions
   - Mock Docker calls
   - Faster execution

2. **Performance Tests**
   - Measure scan duration
   - Track image size
   - Memory usage

3. **Stress Tests**
   - Large projects (1000+ dependencies)
   - Parallel execution
   - Resource limits

4. **Security Tests**
   - Vulnerability scanning
   - Container security
   - Permission checks

## References

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Bash Testing Framework](https://github.com/bats-core/bats-core)
- [Docker Test Containers](https://www.testcontainers.org/)

## Contributing

When adding tests:
1. Follow the template
2. Add clear descriptions
3. Validate edge cases
4. Update this guide
5. Add to CI/CD if needed

See [CONTRIBUTING.md](CONTRIBUTING.md) for more details.
