# Docker Build Optimization Strategy

## Current Status ✅

Your workflow is **already optimized**! It only builds when:

```yaml
on:
  push:
    branches: [ main ]
    paths:                        # ✅ Already optimized
      - 'docker/**'
      - 'scripts/scan-sbom.sh'
      - '.github/workflows/docker-publish.yml'
```

**This means Docker image is only built when:**
- ✅ Docker-related files change (`docker/Dockerfile`, `docker/entrypoint.sh`)
- ✅ Main scan script changes (`scripts/scan-sbom.sh`)
- ✅ Docker workflow itself changes
- ✅ Version tags are pushed (`v*.*.*`)
- ✅ Releases are published

**Docker image is NOT built when:**
- ❌ Documentation changes (README.md, docs/*)
- ❌ Test scripts change (tests/*)
- ❌ Example projects change (examples/*)
- ❌ CI workflow changes (.github/workflows/ci.yml)

## Current Build Frequency Analysis

### Scenario Analysis

| Change Type | Docker Build? | Reason |
|------------|--------------|---------|
| 📝 Update README.md | ❌ No | Not in paths filter |
| 📝 Update docs/ | ❌ No | Not in paths filter |
| 🧪 Update tests/ | ❌ No | Not in paths filter |
| 📦 Update examples/ | ❌ No | Not in paths filter |
| 🐳 Update Dockerfile | ✅ Yes | In paths filter |
| 📜 Update entrypoint.sh | ✅ Yes | In paths filter |
| 📜 Update scan-sbom.sh | ✅ Yes | In paths filter |
| 🏷️ Push v1.0.0 tag | ✅ Yes | Tag trigger |

**Estimated build frequency:** 1-2 times per week (only when Docker components change)

## Recommended Improvements

### Option 1: Current Setup is Good ⭐ (Recommended)

**Keep as-is** - Already well optimized!

**Why:**
- Only builds when Docker image actually needs updating
- Saves ~15-20 minutes per unnecessary build
- Saves GitHub Actions minutes

**No changes needed.**

---

### Option 2: Add Manual Approval for Docker Builds

Add an approval step before pushing to registry:

```yaml
jobs:
  build:
    name: Multi-platform Build
    runs-on: ubuntu-latest
    environment: docker-production  # ← Add this
    permissions:
      contents: read
      packages: write
```

Then configure in GitHub:
1. Settings → Environments → New environment "docker-production"
2. Add required reviewers
3. Every Docker build requires manual approval

**Pros:**
- ✅ Extra control over what gets deployed
- ✅ Good for critical production systems

**Cons:**
- ❌ Slows down deployment
- ❌ Requires manual intervention
- ❌ Overkill for most projects

**Recommended for:** Critical enterprise systems only

---

### Option 3: Separate `latest` and Versioned Releases

**Strategy:**
- `latest` tag: Auto-deploy on main branch (for testing)
- Versioned tags: Only on releases (for production)

**Current behavior:**
```yaml
tags: |
  type=raw,value=latest,enable={{is_default_branch}}  # Already does this!
  type=semver,pattern={{version}}
```

**This already works correctly:**
- Push to main → Updates `latest` only
- Push v1.0.0 tag → Creates `v1.0.0`, `v1.0`, `v1`, and updates `latest`

**Recommendation in scan-sbom.sh:**
```bash
# For testing/development
DOCKER_IMAGE="ghcr.io/sktelecom/sbom-scanner:latest"

# For production users (after first release)
DOCKER_IMAGE="ghcr.io/sktelecom/sbom-scanner:v1"
```

**No changes needed** - already optimal!

---

### Option 4: Reduce Build Paths (More Aggressive)

**Remove `scan-sbom.sh` from paths:**

```yaml
on:
  push:
    branches: [ main ]
    paths:
      - 'docker/**'              # Keep
      # - 'scripts/scan-sbom.sh'  # Remove - doesn't affect image
      - '.github/workflows/docker-publish.yml'
```

**Reasoning:**
- `scan-sbom.sh` runs on user's machine, not inside Docker image
- Changes to `scan-sbom.sh` don't require rebuilding Docker image
- Docker image only needs rebuild when `entrypoint.sh` or `Dockerfile` changes

**Pros:**
- ✅ Even fewer builds
- ✅ Faster CI pipeline

**Cons:**
- ⚠️ If users download old script + new image, might have compatibility issues
- ⚠️ Better to keep synchronized

**Recommendation:** Keep `scan-sbom.sh` in paths (current setup is better)

---

## Build Frequency Comparison

### Before Optimization (if you had no paths filter)

| Week | Changes | Builds | Time Wasted |
|------|---------|--------|------------|
| 1 | 5 doc updates, 1 Docker update | 6 | 100 min |
| 2 | 3 test updates, 2 doc updates | 5 | 80 min |
| 3 | 1 Docker update, 4 doc updates | 5 | 80 min |
| **Total** | | **16** | **260 min** |

### After Optimization (current setup with paths)

| Week | Changes | Builds | Time Saved |
|------|---------|--------|-----------|
| 1 | 5 doc updates, 1 Docker update | 1 | ✅ 100 min |
| 2 | 3 test updates, 2 doc updates | 0 | ✅ 100 min |
| 3 | 1 Docker update, 4 doc updates | 1 | ✅ 80 min |
| **Total** | | **2** | **✅ 280 min** |

**Savings:** ~87.5% fewer builds!

---

## Additional Optimization: Build Cache

Your workflow already uses build cache:

```yaml
cache-from: type=gha
cache-to: type=gha,mode=max
```

**This means:**
- First build: ~15-20 minutes
- Subsequent builds: ~5-10 minutes (using cache)

**Already optimal!** ✅

---

## Monitoring Build Frequency

Check your actual build frequency:

```bash
# Via GitHub API
gh api repos/sktelecom/sbom-tools/actions/workflows/docker-publish.yml/runs \
  --jq '.workflow_runs[] | {created_at, conclusion}'

# Or check manually
# https://github.com/sktelecom/sbom-tools/actions/workflows/docker-publish.yml
```

**Expected:** 1-2 builds per week (only when Docker components change)

---

## Recommendations by Project Stage

### Current Stage: Pre-release / Active Development

**Keep current setup** - Already optimal!

```yaml
on:
  push:
    branches: [ main ]
    paths:
      - 'docker/**'
      - 'scripts/scan-sbom.sh'
      - '.github/workflows/docker-publish.yml'
```

**Why:**
- ✅ Only builds when necessary
- ✅ Fast iteration on Docker changes
- ✅ Saves CI minutes on docs/tests

---

### Future Stage: Stable Production

**Consider:** Only build on tags + manual trigger

```yaml
on:
  # Remove automatic main branch builds
  # push:
  #   branches: [ main ]
  
  # Keep tag-based builds for releases
  tags:
    - 'v*.*.*'
  
  # Keep manual trigger for emergencies
  workflow_dispatch:
```

**Pros:**
- ✅ Even fewer builds
- ✅ More controlled releases
- ✅ Production-grade stability

**Cons:**
- ⚠️ Slower iteration
- ⚠️ Must create tags for new features

**When to switch:** After v1.0.0 stable release

---

## Summary & Recommendation

### ✅ Current Status: Already Excellent!

Your setup is **already well-optimized**. No immediate changes needed.

**Current behavior:**
- Builds only when Docker components change
- Uses build cache for speed
- Separates `latest` (testing) from versioned tags (production)

### 📊 Statistics

- **Build frequency:** 1-2 per week (optimal)
- **Time saved:** ~87% vs unoptimized
- **Cost saved:** ~$0 (within free tier)

### 🎯 Action Items

1. **Immediate:** No changes needed - current setup is optimal
2. **Before v1.0.0 release:**
   - Decide on `latest` vs `v1` tag strategy for scan-sbom.sh
   - Create first release tag to generate `v1` tag
3. **After stable release:**
   - Consider switching to tag-only builds (optional)
   - Monitor build frequency and adjust if needed

### 🔧 Optional Tweak

If you want even fewer builds, remove `scan-sbom.sh` from paths:

```diff
  paths:
    - 'docker/**'
-   - 'scripts/scan-sbom.sh'
    - '.github/workflows/docker-publish.yml'
```

But current setup is better for keeping script/image synchronized.

---

## Conclusion

**Your Docker build strategy is already well-optimized.** 🎉

No changes needed unless you want to be even more conservative after the stable release.
