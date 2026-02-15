# Documentation Updates for Version Control Feature

## Changes Made

Both README files have been updated with a new "Advanced Usage" section.

### Files Updated

1. ✅ **README.md** (English)
2. ✅ **README.ko.md** (Korean)

## New Section: Advanced Usage

### What's Added

A new section explaining:
- **Docker Image Version Control**: How to pin to specific versions
- **Version Strategy**: Which version to use for different scenarios
- **Windows Usage**: How to use the feature on Windows

### Content Structure

```
## Advanced Usage

### Docker Image Version Control
- Default behavior (latest)
- Pin to v1 family
- Pin to exact version

**Version Strategy:**
- latest - Development
- v1 - CI/CD
- v1.0 - Stable production
- v1.0.0 - Maximum stability

### Windows Usage
- Download instructions
- Basic usage
- Version pinning example
```

## Why This Matters

### User Benefits

✅ **Clear Guidance**: Users know how to choose versions
✅ **Production Safety**: Clear recommendation for stable deployments
✅ **Flexibility**: Understand trade-offs of each version strategy
✅ **Platform Coverage**: Both Linux/macOS and Windows instructions

### Documentation Completeness

Before:
- ❌ No mention of version control
- ❌ Users don't know about `latest` vs `v1`
- ❌ No Windows usage examples

After:
- ✅ Complete version control documentation
- ✅ Clear version strategy recommendations
- ✅ Windows-specific instructions

## Location in README

The new section appears after "Usage Examples" and before "Documentation":

```
## Quick Start
## Usage Examples
## Advanced Usage  ← NEW
## Documentation
## Architecture
```

This placement makes sense because:
- Users learn basic usage first
- Then discover advanced features
- Finally dive into detailed docs

## Examples from README

### English Version

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

### Korean Version

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

## Version Strategy Table

Both READMEs now include this guidance:

| Version | Use Case | Update Frequency |
|---------|----------|------------------|
| `latest` | Development | Every release |
| `v1` | CI/CD | Minor + Patch updates |
| `v1.0` | Stable Production | Patch updates only |
| `v1.0.0` | Maximum Stability | Never changes |

## Windows-Specific Section

Added Windows instructions that were previously missing:

```cmd
REM Download script
curl -O https://raw.githubusercontent.com/sktelecom/sbom-tools/main/scripts/scan-sbom.bat

REM Default usage
scan-sbom.bat --project "MyApp" --version "1.0.0" --generate-only

REM Pin to specific version
set SBOM_SCANNER_IMAGE=ghcr.io/sktelecom/sbom-scanner:v1
scan-sbom.bat --project "MyApp" --version "1.0.0" --generate-only
```

## Impact on User Experience

### Before Documentation Update

User: "How do I ensure my production builds are stable?"
Answer: Not documented ❌

User: "Does this work on Windows?"
Answer: Not clear ❌

User: "What's the difference between latest and v1?"
Answer: Not explained ❌

### After Documentation Update

User: "How do I ensure my production builds are stable?"
Answer: Use `v1.0.0` for exact version ✅

User: "Does this work on Windows?"
Answer: Yes, here's how (with examples) ✅

User: "What's the difference between latest and v1?"
Answer: Clear table with recommendations ✅

## Consistency Check

✅ **English and Korean versions are consistent**
- Same content structure
- Same examples (translated)
- Same recommendations
- Same version strategy table

✅ **Aligned with script help text**
- Script `--help` mentions `SBOM_SCANNER_IMAGE`
- README explains how to use it
- Examples match script capabilities

✅ **Aligned with Docker deployment strategy**
- README recommends `latest` by default
- Matches default in scripts
- Explains when to use other tags

## Next Steps

### For First Release (v1.0.0)

When you create the first release:

1. Users can immediately use `latest` (already works)
2. After v1.0.0 release, they can switch to `v1` if desired
3. Documentation already explains all options

### Future Documentation

Consider adding to detailed docs:
- Troubleshooting section for version mismatches
- Migration guide when major versions change (v1 → v2)
- Best practices for enterprise deployments

## Summary

| What | Status | Impact |
|------|--------|--------|
| README.md | ✅ Updated | Users know how to control versions |
| README.ko.md | ✅ Updated | Korean users have same info |
| Advanced Usage section | ✅ Added | Clear version strategy |
| Windows instructions | ✅ Added | Platform complete |
| Version strategy table | ✅ Added | Decision making guide |

**Result:** Users now have complete documentation for version control feature! 📚✨
