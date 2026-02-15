# 테스트 문제 해결 가이드

## 발생한 문제

### 1. GitHub Actions - validate-examples 실패

**에러 메시지**:
```
Run cd examples/java-maven
test -f pom.xml
test -f src/main/java/com/example/Application.java
test -f README.md
Error: Process completed with exit code 1.
```

**원인**: 파일 자체는 존재하지만 GitHub에 푸시할 때 중간 디렉토리가 제대로 생성되지 않았을 가능성

**해결 방법**:

#### 옵션 1: .gitkeep 파일 추가 (권장)

빈 디렉토리를 Git이 추적하도록 하기 위해 각 중간 디렉토리에 `.gitkeep` 파일을 추가합니다.

```bash
cd sbom-tools

# Java 예제 디렉토리 구조 보장
touch examples/java-maven/src/.gitkeep
touch examples/java-maven/src/main/.gitkeep
touch examples/java-maven/src/main/java/.gitkeep
touch examples/java-maven/src/main/java/com/.gitkeep
touch examples/java-maven/src/main/java/com/example/.gitkeep

# Git 추가 및 커밋
git add examples/java-maven/src
git commit -m "fix: Add .gitkeep files to preserve Java directory structure"
git push origin main
```

#### 옵션 2: 파일 구조 확인 후 재커밋

```bash
# 현재 상태 확인
cd sbom-tools
find examples/java-maven -type f

# 다시 추가 및 커밋
git add examples/java-maven/
git commit -m "fix: Ensure all Java example files are tracked"
git push origin main
```

### 2. 로컬 테스트 - Test 10 실패

**에러**: 예제 프로젝트 검증 3/4 완료

**원인**: 
1. `EXAMPLES_DIR` 변수가 정의되지 않았음
2. 테스트 실행 중 현재 디렉토리가 변경되어 상대 경로 문제 발생

**해결**: 
테스트 스크립트를 수정하여 `$ROOT_DIR`을 기준으로 절대 경로 사용하도록 변경 완료

## 수정된 파일

### tests/test-scan.sh

다음 두 가지 수정사항:

1. **EXAMPLES_DIR 변수 추가**:
```bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
TEST_DIR="$SCRIPT_DIR/test-workspace"
SCAN_SCRIPT="$ROOT_DIR/scripts/scan-sbom.sh"
EXAMPLES_DIR="$ROOT_DIR/examples"  # 추가됨
```

2. **예제 검증 로직 개선**:
- `$ROOT_DIR`로 명시적으로 이동
- 상대 경로 "examples/"로 통일
- 더 명확한 파일 존재 확인 로직

## 검증 방법

### 로컬 테스트

```bash
cd sbom-tools
chmod +x tests/test-scan.sh
./tests/test-scan.sh
```

**예상 결과**:
```
[TEST] Test 10/10: 예제 프로젝트 검증
[✓] 예제 프로젝트 (4/4 완료)

==========================================
 테스트 결과 요약
==========================================

총 테스트: 10
통과: 10
실패: 0
성공률: 100.0%
```

### GitHub Actions 재실행

1. 수정된 파일 커밋 및 푸시:
```bash
git add tests/test-scan.sh
git add examples/  # .gitkeep 파일 추가한 경우
git commit -m "fix: Fix test script and Java example directory structure"
git push origin main
```

2. GitHub Actions 자동 실행 확인
3. 또는 수동 실행: Actions → CI → Run workflow

## 추가 확인 사항

### Java 예제 파일 구조 확인

```bash
cd sbom-tools
find examples/java-maven -type f
```

**예상 출력**:
```
examples/java-maven/pom.xml
examples/java-maven/README.md
examples/java-maven/src/main/java/com/example/Application.java
examples/java-maven/src/.gitkeep          # 옵션 1 선택 시
examples/java-maven/src/main/.gitkeep     # 옵션 1 선택 시
examples/java-maven/src/main/java/.gitkeep
examples/java-maven/src/main/java/com/.gitkeep
examples/java-maven/src/main/java/com/example/.gitkeep
```

### 파일 내용 확인

```bash
# Application.java가 비어있지 않은지 확인
cat examples/java-maven/src/main/java/com/example/Application.java | wc -l
```

출력이 0이 아니어야 합니다 (약 30줄 예상).

## GitHub에서 확인

1. https://github.com/haksungjang/sbom-tools/tree/main/examples/java-maven 접속
2. src 디렉토리 클릭하여 구조 확인
3. Application.java까지 이동 가능한지 확인

만약 파일이 보이지 않으면:
- 로컬에서 `git add -f examples/java-maven/` 실행
- 커밋 후 다시 푸시

## 최종 확인 스크립트

다음 스크립트로 모든 예제 파일이 존재하는지 한 번에 확인:

```bash
#!/bin/bash

echo "예제 파일 존재 확인..."

FILES=(
  "examples/java-maven/pom.xml"
  "examples/java-maven/src/main/java/com/example/Application.java"
  "examples/java-maven/README.md"
  "examples/python/requirements.txt"
  "examples/python/app.py"
  "examples/python/README.md"
  "examples/nodejs/package.json"
  "examples/nodejs/index.js"
  "examples/nodejs/README.md"
  "examples/docker/Dockerfile"
  "examples/docker/README.md"
)

MISSING=0
for file in "${FILES[@]}"; do
  if [ -f "$file" ]; then
    echo "✓ $file"
  else
    echo "✗ $file (누락)"
    ((MISSING++))
  fi
done

echo ""
if [ $MISSING -eq 0 ]; then
  echo "✅ 모든 예제 파일 존재 확인 완료!"
else
  echo "❌ $MISSING 개 파일 누락"
  exit 1
fi
```

이 스크립트를 `check-examples.sh`로 저장하고 실행:

```bash
chmod +x check-examples.sh
./check-examples.sh
```

## 권장 조치

### 즉시 실행

```bash
cd sbom-tools

# .gitkeep 파일 추가
find examples/java-maven/src -type d -exec touch {}/.gitkeep \;

# Git 추가
git add examples/
git add tests/test-scan.sh

# 커밋
git commit -m "fix: Fix example directory structure and test script

- Add .gitkeep files to preserve Java directory structure
- Fix EXAMPLES_DIR variable in test script
- Improve example validation logic"

# 푸시
git push origin main
```

### 확인

1. GitHub Actions 자동 실행 대기 (약 5분)
2. 모든 Job이 통과하는지 확인
3. 로컬에서 다시 테스트: `./tests/test-scan.sh`

---

**문제가 계속되면**:

1. 로컬에서 파일 존재 확인:
   ```bash
   ls -laR examples/java-maven/
   ```

2. Git 추적 상태 확인:
   ```bash
   git ls-files examples/java-maven/
   ```

3. 강제로 다시 추가:
   ```bash
   git rm -r --cached examples/java-maven/
   git add examples/java-maven/
   git commit -m "fix: Re-add Java example files"
   git push
   ```
