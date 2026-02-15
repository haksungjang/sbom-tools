# Script Updates Summary

## Changes Made

Both `scan-sbom.sh` and `scan-sbom.bat` have been updated with:

### 1. Flexible Docker Image Selection

**Before:**
```bash
# Hardcoded version
DOCKER_IMAGE="ghcr.io/sktelecom/sbom-scanner:v1"
```

**After:**
```bash
# Environment variable with default
DOCKER_IMAGE="${SBOM_SCANNER_IMAGE:-ghcr.io/sktelecom/sbom-scanner:latest}"
```

### 2. Enhanced Help Documentation

Both scripts now include environment variable documentation in `--help`:

```
Environment Variables:
  SBOM_SCANNER_IMAGE     Docker image to use (default: latest)
                         Examples:
                           ghcr.io/sktelecom/sbom-scanner:latest (default)
                           ghcr.io/sktelecom/sbom-scanner:v1
                           ghcr.io/sktelecom/sbom-scanner:v1.0.0
```

## Usage Examples

### Default Usage (latest version)

**Linux/macOS:**
```bash
./scan-sbom.sh --project MyApp --version 1.0.0 --generate-only
```

**Windows:**
```cmd
scan-sbom.bat --project MyApp --version 1.0.0 --generate-only
```

### Pin to Specific Version

**Linux/macOS:**
```bash
# Use v1 family (latest v1.x.x)
SBOM_SCANNER_IMAGE=ghcr.io/sktelecom/sbom-scanner:v1 \
  ./scan-sbom.sh --project MyApp --version 1.0.0 --generate-only

# Use exact version
SBOM_SCANNER_IMAGE=ghcr.io/sktelecom/sbom-scanner:v1.0.0 \
  ./scan-sbom.sh --project MyApp --version 1.0.0 --generate-only
```

**Windows:**
```cmd
REM Use v1 family
set SBOM_SCANNER_IMAGE=ghcr.io/sktelecom/sbom-scanner:v1
scan-sbom.bat --project MyApp --version 1.0.0 --generate-only

REM Use exact version
set SBOM_SCANNER_IMAGE=ghcr.io/sktelecom/sbom-scanner:v1.0.0
scan-sbom.bat --project MyApp --version 1.0.0 --generate-only
```

## Benefits

### For Users

✅ **Automatic Updates**: Default to `latest` ensures users get newest features
✅ **Production Safety**: Can pin to specific versions for stability
✅ **Flexibility**: Choose update strategy that fits your needs
✅ **Clear Documentation**: Help text explains all options

### For Developers

✅ **No Hardcoding**: Easy to change default version
✅ **Testing**: Can test different image versions easily
✅ **Compatibility**: Scripts work even before v1 tag exists

## Version Strategy Recommendations

| Use Case | Recommended Tag | Why |
|----------|----------------|-----|
| Development/Testing | `latest` | Always get newest features |
| CI/CD Pipeline | `v1` | Get patches/features, avoid breaking changes |
| Production (Strict) | `v1.0.0` | Exact version, maximum stability |
| Production (Flexible) | `v1.0` | Get patches, avoid feature changes |

## Help Text Access

Both scripts now document this feature:

```bash
# Linux/macOS
./scan-sbom.sh --help

# Windows
scan-sbom.bat --help
```

## Files Updated

- ✅ `scripts/scan-sbom.sh` - Linux/macOS script
- ✅ `scripts/scan-sbom.bat` - Windows script

Both scripts now have identical functionality and documentation!
