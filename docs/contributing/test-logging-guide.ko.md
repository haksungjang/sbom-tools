# Test Logging Feature Guide

## Overview

The test suite now includes comprehensive logging capabilities to help debug test failures.

## Usage Modes

### 1. Normal Mode (Quiet)

**Default behavior** - Logs saved to files, shown only on failure:

```bash
./tests/test-scan.sh
```

**Output:**
```
🔇 Quiet Mode: 활성화 (로그는 파일에 저장됨)
   실패 시 자동으로 로그 표시됨

[TEST] Test 1/10: Node.js project (npm)
[✓] Node.js project (69 components)

[TEST] Test 3/10: Java Maven project
[✗] Java Maven project (SBOM이 비어있음)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
실패한 테스트 로그: test-java-maven
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[INFO] Found pom.xml. Processing Maven dependencies...
[INFO] Downloading dependencies...
[ERROR] Maven build failed
...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
전체 로그: tests/test-workspace/logs/test-java-maven.log
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 2. Verbose Mode

**Show key messages** during test execution:

```bash
VERBOSE=true ./tests/test-scan.sh
```

**Output shows:**
- `[INFO]` messages from entrypoint.sh
- `[WARN]` warnings
- `[ERROR]` errors
- cdxgen/syft key operations
- Component counts

**Good for:** Monitoring progress without overwhelming output

### 3. Debug Mode

**Show everything** in real-time + preserve workspace:

```bash
DEBUG_MODE=true ./tests/test-scan.sh
```

**Shows:**
- All Docker container output
- cdxgen detailed logs
- syft scanning progress
- Maven/Gradle build output
- File operations

**Preserves:**
- Test workspace at `tests/test-workspace/`
- All intermediate files
- Generated SBOMs

**Good for:** Deep debugging, understanding what's happening

## Log Files

### During Test Run

All logs saved to: `tests/test-workspace/logs/`

Files:
```
tests/test-workspace/logs/
├── test-nodejs.log
├── test-python.log
├── test-java-maven.log
├── test-ruby.log
├── test-php.log
├── test-rust.log
├── test-docker-image.log
├── test-binary.log
├── test-rootfs.log
└── test-examples.log
```

### After Test Failure

Failed test logs copied to: `tests/test-workspace/failed-tests-logs/`

This directory persists even after cleanup, so you can review logs later.

## Examples

### Example 1: Quick Test with Auto-Debug

```bash
# Run tests normally
./tests/test-scan.sh

# If a test fails, logs are automatically shown
# Review the specific log file
cat tests/test-workspace/failed-tests-logs/test-java-maven.log
```

### Example 2: Monitor Progress

```bash
# Show key messages during execution
VERBOSE=true ./tests/test-scan.sh
```

**Output:**
```
[INFO] Found pom.xml. Processing Maven dependencies...
[INFO] Downloading dependencies...
[INFO] Downloaded JARs: 87
[INFO] SBOM generated: TestJavaMaven_1.0.0_bom.json
```

### Example 3: Deep Debugging

```bash
# Full debug mode
DEBUG_MODE=true ./tests/test-scan.sh

# After test, workspace is preserved
ls -la tests/test-workspace/
cd tests/test-workspace/java-maven-project/
cat TestJavaMaven_1.0.0_bom.json
```

### Example 4: Check Specific Test Log

```bash
# Run tests
./tests/test-scan.sh

# Review specific test log
cat tests/test-workspace/logs/test-java-maven.log | grep -A 5 "ERROR"
```

## Log Content

### What's Logged

Each log file contains:

1. **Scan initialization**
   ```
   ==========================================
     Starting SBOM Analysis
     Mode: SOURCE
     Project: TestJavaMaven (1.0.0)
   ==========================================
   ```

2. **Environment detection**
   ```
   [INFO] JAVA_HOME detected: /usr/lib/jvm/temurin-17-jdk-amd64
   [INFO] Java verified: openjdk version "17.0.10"
   ```

3. **Dependency resolution**
   ```
   [INFO] Found pom.xml. Processing Maven dependencies...
   [INFO] Generating effective POM...
   [INFO] Downloading dependencies...
   ```

4. **SBOM generation**
   ```
   [cdxgen] Analyzing project...
   [cdxgen] Found 87 components
   [INFO] SBOM generated: TestJavaMaven_1.0.0_bom.json
   ```

5. **Errors (if any)**
   ```
   [ERROR] Maven dependency download failed
   [WARN] Some packages may be missing
   ```

## Troubleshooting

### No Logs Generated

**Issue:** Logs directory is empty

**Solution:**
```bash
# Check if LOG_DIR is set
echo $LOG_DIR

# Manually create
mkdir -p tests/test-workspace/logs

# Run test again
./tests/test-scan.sh
```

### Logs Too Large

**Issue:** Log files are several MB

**Solution:**
```bash
# View last 100 lines only
tail -100 tests/test-workspace/logs/test-java-maven.log

# Search for errors
grep -i error tests/test-workspace/logs/test-java-maven.log

# Filter for important messages
grep -E '\[INFO\]|\[WARN\]|\[ERROR\]' tests/test-workspace/logs/test-java-maven.log
```

### Can't Find Failed Logs

**Issue:** `failed-tests-logs` directory doesn't exist

**Reason:** No tests failed!

**Verify:**
```bash
# Check test results
./tests/test-scan.sh
# Look for "Failed: 0"
```

## Integration with CI/CD

### GitHub Actions

```yaml
- name: Run tests with logging
  run: |
    VERBOSE=true ./tests/test-scan.sh
  
- name: Upload logs on failure
  if: failure()
  uses: actions/upload-artifact@v4
  with:
    name: test-logs
    path: tests/test-workspace/logs/
```

### Local Development

```bash
# During development
DEBUG_MODE=true ./tests/test-scan.sh

# Before committing
VERBOSE=true ./tests/test-scan.sh

# In CI/CD
./tests/test-scan.sh  # Quiet mode, logs on failure
```

## Advanced Usage

### Custom Log Analysis

```bash
# Extract all errors from all logs
grep -r "\[ERROR\]" tests/test-workspace/logs/

# Find which test took longest
for log in tests/test-workspace/logs/*.log; do
  echo "$log: $(grep "Analysis Complete" $log)"
done

# Check component counts
for log in tests/test-workspace/logs/*.log; do
  echo "$log: $(grep -o "[0-9]* components" $log)"
done
```

### Selective Debugging

```bash
# Debug only Java tests
DEBUG_MODE=true ./tests/test-scan.sh 2>&1 | grep -A 20 "Java Maven"

# Verbose for specific stages
VERBOSE=true ./tests/test-scan.sh 2>&1 | tee full-test-output.log
```

## Implementation Details

### Functions Added

1. **run_scan_with_logs()**
   - Executes scan with appropriate output level
   - Saves logs to file
   - Supports DEBUG, VERBOSE, and quiet modes

2. **show_failure_log()**
   - Automatically displays log on test failure
   - Shows last 50 lines or full log
   - Provides log file path for reference

3. **cleanup()**
   - Preserves failed test logs
   - Cleans up successful test files
   - Keeps workspace in debug mode

### Environment Variables

- `DEBUG_MODE` - Full output + preserve workspace
- `VERBOSE` - Show key messages only
- `LOG_DIR` - Log directory location (auto-set)

## Tips

1. **Start with normal mode** - Fastest, shows issues automatically
2. **Use verbose for monitoring** - See progress without noise
3. **Use debug for deep issues** - When you need to see everything
4. **Check failed-tests-logs** - After test run, review failures
5. **Grep logs for errors** - Quick way to find problems

## Help

```bash
# Show help
./tests/test-scan.sh --help

# Example output
Usage: ./test-scan.sh [OPTIONS]

Options:
  --help, -h          Show this help message
  
Environment Variables:
  DEBUG_MODE=true     Enable debug mode
  VERBOSE=true        Enable verbose mode
  
Examples:
  ./test-scan.sh                    # Normal mode
  VERBOSE=true ./test-scan.sh       # Verbose mode
  DEBUG_MODE=true ./test-scan.sh    # Debug mode
```

## Summary

| Mode | Command | Output | Logs | Workspace |
|------|---------|--------|------|-----------|
| **Normal** | `./test-scan.sh` | Quiet, show on fail | Saved | Cleaned |
| **Verbose** | `VERBOSE=true ./test-scan.sh` | Key messages | Saved | Cleaned |
| **Debug** | `DEBUG_MODE=true ./test-scan.sh` | Everything | Saved | Preserved |

**Default:** Normal mode - quiet operation, automatic debug on failure

**Recommended:** Start with normal, use verbose/debug as needed
