# Docker Image Size Optimization Strategy

## Current Problem

**Current size:** 7.3 GB ❌  
**Target size:** < 2 GB ✅

## Root Causes Analysis

### 1. Multiple JDK Versions (Biggest culprit)
```dockerfile
temurin-21-jdk temurin-17-jdk temurin-11-jdk temurin-8-jdk
```
**Size impact:** ~3-4 GB
- Each JDK: ~300-500 MB
- 4 JDKs: ~1.5-2 GB
- Plus dependencies

**Question:** Do we really need all 4 JDK versions?

### 2. Base Image
```dockerfile
FROM node:20-bookworm
```
**Size impact:** ~1 GB
- Full Debian base
- Node.js included

**Alternative:** Use Alpine base (~200 MB)

### 3. Build Tools
```dockerfile
build-essential gcc g++ make cmake autoconf automake libtool pkg-config
```
**Size impact:** ~500 MB
- Needed for compilation
- But rarely used for SBOM scanning

### 4. Multiple Language Runtimes
- Python 2 + Python 3
- Ruby + Bundler
- PHP + Composer
- Rust toolchain

**Combined impact:** ~1-2 GB

## Optimization Strategies

### Strategy 1: Use Only One JDK Version (Quick Win) ⭐

**Recommendation:** Keep only JDK 17 (LTS)

```dockerfile
# Before (4 JDKs)
temurin-21-jdk temurin-17-jdk temurin-11-jdk temurin-8-jdk

# After (1 JDK)
temurin-17-jdk
```

**Reasoning:**
- JDK 17 can compile/analyze projects built with Java 7-17
- Most modern projects use Java 11 or 17
- Java 8 and 21 are less critical for SBOM generation

**Size reduction:** ~1.5 GB saved

---

### Strategy 2: Multi-Stage Build

**Current:** Everything in one layer  
**Better:** Build tools in separate stage

```dockerfile
# Stage 1: Build tools (heavy)
FROM node:20-bookworm AS builder
# Install all build tools here

# Stage 2: Runtime (light)
FROM node:20-slim
# Copy only necessary binaries from builder
COPY --from=builder /usr/local/bin/cdxgen /usr/local/bin/
```

**Size reduction:** ~500 MB - 1 GB saved

---

### Strategy 3: Switch to Alpine Base ⭐⭐

**Current:** Debian bookworm (~1 GB)  
**Alternative:** Alpine (~200 MB)

```dockerfile
FROM node:20-alpine
```

**Challenges:**
- Need to install packages differently (apk instead of apt-get)
- Some packages have different names
- May need musl-compat for some tools

**Size reduction:** ~800 MB saved

---

### Strategy 4: Remove Unnecessary Tools

**Build tools (rarely needed for SBOM):**
```dockerfile
# Remove or move to multi-stage
build-essential gcc g++ make cmake autoconf automake libtool pkg-config
binutils binwalk
```

**Python 2 (legacy, 2020 EOL):**
```dockerfile
# Remove unless you have specific legacy projects
python2 python2-dev
```

**Size reduction:** ~700 MB saved

---

### Strategy 5: Use Slim Variants

**Language runtimes:**
- Use `python:3-slim` instead of full Python
- Use minimal PHP installation
- Use smaller Ruby distribution

**Size reduction:** ~300-500 MB saved

---

## Recommended Approach (Balanced)

Combine multiple strategies for best results:

### Phase 1: Quick Wins (Immediate)

1. **Keep only JDK 17** (remove 8, 11, 21)
2. **Remove Python 2** (unless specifically needed)
3. **Remove build-essential** (most SBOM tools don't need compilation)
4. **Use node:20-slim** instead of node:20-bookworm

**Expected size:** ~3-4 GB (50% reduction)

### Phase 2: Major Optimization (If needed)

5. **Switch to Alpine base**
6. **Multi-stage build**
7. **Lazy install languages** (only install when detected)

**Expected size:** ~1.5-2 GB (70-75% reduction)

---

## Optimized Dockerfile (Phase 1)

```dockerfile
# Use slim base
FROM node:20-slim

ENV DEBIAN_FRONTEND=noninteractive

# Essential tools only
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl bash jq git wget ca-certificates gnupg \
    file procps \
    && rm -rf /var/lib/apt/lists/*

# Python 3 (slim)
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Single JDK (Java 17 LTS)
RUN mkdir -p /etc/apt/keyrings \
    && wget -qO - https://packages.adoptium.net/artifactory/api/gpg/key/public | tee /etc/apt/keyrings/adoptium.asc \
    && echo "deb [signed-by=/etc/apt/keyrings/adoptium.asc] https://packages.adoptium.net/artifactory/deb $(awk -F= '/^VERSION_CODENAME/{print$2}' /etc/os-release) main" | tee /etc/apt/sources.list.d/adoptium.list \
    && apt-get update && apt-get install -y --no-install-recommends \
    temurin-17-jdk \
    && rm -rf /var/lib/apt/lists/*

# Maven & Gradle (lightweight install)
RUN apt-get update && apt-get install -y --no-install-recommends \
    maven \
    && rm -rf /var/lib/apt/lists/* \
    && wget -q https://services.gradle.org/distributions/gradle-8.5-bin.zip \
    && unzip -q gradle-8.5-bin.zip -d /opt \
    && ln -s /opt/gradle-8.5/bin/gradle /usr/local/bin/gradle \
    && rm gradle-8.5-bin.zip

# Ruby (slim)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ruby ruby-dev bundler \
    && rm -rf /var/lib/apt/lists/*

# PHP (minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    php-cli php-xml php-mbstring composer \
    && rm -rf /var/lib/apt/lists/*

# Rust (slim install)
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y \
    --default-toolchain stable --profile minimal --no-modify-path

# Docker CLI (for image scanning)
RUN install -m 0755 -d /etc/apt/keyrings \
    && curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc \
    && chmod a+r /etc/apt/keyrings/docker.asc \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
    $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null \
    && apt-get update \
    && apt-get install -y --no-install-recommends docker-ce-cli \
    && rm -rf /var/lib/apt/lists/*

# SBOM tools
RUN npm install -g @cyclonedx/cdxgen \
    && curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s -- -b /usr/local/bin

# Environment
ENV PATH="/root/.cargo/bin:${PATH}"
ENV JAVA_HOME="/usr/lib/jvm/temurin-17-jdk-$(dpkg --print-architecture)"

# Entrypoint
COPY entrypoint.sh /usr/local/bin/run-scan
RUN chmod +x /usr/local/bin/run-scan

WORKDIR /src
ENTRYPOINT ["/usr/local/bin/run-scan"]
```

**Expected size:** ~3-4 GB

---

## Even Smaller: Alpine-based (Phase 2)

```dockerfile
FROM node:20-alpine

# Install runtime dependencies
RUN apk add --no-cache \
    bash curl wget git jq \
    openjdk17 maven \
    python3 py3-pip \
    ruby ruby-dev ruby-bundler \
    php82 php82-xml php82-mbstring composer \
    docker-cli \
    file

# Install Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y \
    --profile minimal --no-modify-path

# SBOM tools
RUN npm install -g @cyclonedx/cdxgen
RUN wget -qO- https://github.com/anchore/syft/releases/latest/download/syft_linux_amd64.tar.gz | tar xz -C /usr/local/bin

# Environment
ENV PATH="/root/.cargo/bin:${PATH}"
ENV JAVA_HOME="/usr/lib/jvm/java-17-openjdk"

# Entrypoint
COPY entrypoint.sh /usr/local/bin/run-scan
RUN chmod +x /usr/local/bin/run-scan

WORKDIR /src
ENTRYPOINT ["/usr/local/bin/run-scan"]
```

**Expected size:** ~1.5-2 GB

---

## Trade-offs Analysis

### Option 1: Keep 7.3 GB (Current)
**Pros:**
- Supports all Java versions (7-21)
- Maximum compatibility
- No testing needed

**Cons:**
- ❌ Very slow pull (5-10 min on slow connections)
- ❌ Wastes disk space
- ❌ Slower startup
- ❌ Poor user experience

### Option 2: Optimize to 3-4 GB (Phase 1) ⭐
**Pros:**
- ✅ 50% size reduction
- ✅ Still supports Java 7-17
- ✅ Quick to implement
- ✅ Low risk

**Cons:**
- ⚠️ Java 21 projects might need workarounds
- ⚠️ No Python 2 support

**Recommended for:** Immediate improvement

### Option 3: Optimize to 1.5-2 GB (Phase 2)
**Pros:**
- ✅ 75% size reduction
- ✅ Much better user experience
- ✅ Professional image size

**Cons:**
- ⚠️ More testing needed
- ⚠️ Alpine compatibility issues possible
- ⚠️ May need adjustments to entrypoint.sh

**Recommended for:** Next iteration

---

## Compatibility Impact

### Java Version Support

| JDK in Image | Can Analyze |
|--------------|-------------|
| JDK 8 | Java 5-8 |
| JDK 11 | Java 5-11 |
| JDK 17 | Java 7-17 ✅ |
| JDK 21 | Java 7-21 |

**With JDK 17 only:**
- ✅ Covers 95%+ of projects
- ✅ Java 8, 11, 17 projects work fine
- ⚠️ Java 21 projects might have issues
- ❌ Very old Java 6/7 projects might fail

**Mitigation:** Document that JDK 17 is used

---

## Recommendation

### Immediate Action (This Week)

Implement **Phase 1** optimizations:

1. Remove JDK 8, 11, 21 (keep only 17)
2. Remove Python 2
3. Switch to node:20-slim
4. Remove build-essential
5. Remove binwalk, binutils (rarely used)

**Expected result:** 3-4 GB (50% reduction)

### Medium Term (Next Release)

Test **Phase 2** with Alpine:
1. Create alpine branch
2. Build Alpine-based image
3. Test with example projects
4. If successful, make it default

**Expected result:** 1.5-2 GB (75% reduction)

---

## Testing Checklist

After optimization, test:
- [ ] Java Maven project (Java 8)
- [ ] Java Gradle project (Java 17)
- [ ] Python 3.x project
- [ ] Node.js project
- [ ] Ruby project
- [ ] PHP project
- [ ] Rust project
- [ ] Docker image scanning
- [ ] Binary file scanning

---

## User Communication

Update README to mention:
- Image size: ~4 GB (down from 7.3 GB)
- Java 17 JDK included (supports Java 7-17)
- For Java 21 projects, build from source or use JDK 21 image

---

## Implementation Priority

1. **High Priority:** Remove extra JDKs (biggest win)
2. **High Priority:** Switch to slim base
3. **Medium Priority:** Remove Python 2
4. **Medium Priority:** Remove build tools
5. **Low Priority:** Alpine migration (save for later)

Start with high-priority items for immediate 50% reduction!
