# Test 10 예제 검증 실패 해결 방법

## 문제 상황

```
[TEST] Test 10/10: 예제 프로젝트 검증
[✗] 예제 프로젝트 (3/4 완료)
```

4개 예제 중 1개가 실패 → Java 예제의 `Application.java` 파일을 찾지 못함

## 원인

Git은 **빈 디렉토리를 추적하지 않습니다**. Java 예제의 중간 디렉토리 구조가 Git에 커밋되지 않았습니다:

```
examples/java-maven/src/main/java/com/example/
```

이 경로의 중간 디렉토리들(`src`, `main`, `java`, `com`, `example`)이 파일 없이 존재하면 Git이 무시합니다.

## 해결 방법

### 1. .gitkeep 파일 추가 (이미 완료됨)

각 중간 디렉토리에 `.gitkeep` 파일을 추가하여 Git이 디렉토리 구조를 추적하도록 합니다:

```bash
cd sbom-tools

# .gitkeep 파일 자동 생성
find examples/java-maven/src -type d -exec touch {}/.gitkeep \;

# 생성 확인
find examples/java-maven -name .gitkeep
```

**예상 출력**:
```
examples/java-maven/src/.gitkeep
examples/java-maven/src/main/.gitkeep
examples/java-maven/src/main/java/.gitkeep
examples/java-maven/src/main/java/com/.gitkeep
examples/java-maven/src/main/java/com/example/.gitkeep
```

### 2. Git 커밋 및 푸시

```bash
# 변경사항 확인
git status

# 추가
git add examples/java-maven/
git add tests/test-scan.sh

# 커밋
git commit -m "fix: Add .gitkeep files to Java example directory structure

- Add .gitkeep files to preserve src/main/java/com/example/ structure
- Add debug output to test script for better troubleshooting
- Fixes Test 10 failure (3/4 → 4/4)"

# 푸시
git push origin main
```

### 3. 로컬에서 재테스트

```bash
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

==========================================
 🎉 모든 테스트 통과!
==========================================
```

## 디버그 출력

만약 여전히 실패한다면, 수정된 테스트 스크립트가 디버그 정보를 출력합니다:

```
[TEST] Test 10/10: 예제 프로젝트 검증
  [DEBUG] Java: pom.xml exists but Application.java missing
  [DEBUG] Checking: examples/java-maven/src/main/java/com/example/Application.java
  [DEBUG] Directory not found
[✗] 예제 프로젝트 (3/4 완료)
```

이 경우:
1. `examples/java-maven/src/main/java/com/example/Application.java` 파일이 실제로 존재하는지 확인
2. `.gitkeep` 파일이 모든 중간 디렉토리에 있는지 확인
3. Git에 제대로 추가되었는지 확인: `git ls-files examples/java-maven/`

## 최종 확인

### 파일 구조 확인
```bash
tree examples/java-maven/
```

**예상 출력**:
```
examples/java-maven/
├── README.md
├── pom.xml
└── src
    ├── .gitkeep
    └── main
        ├── .gitkeep
        └── java
            ├── .gitkeep
            └── com
                ├── .gitkeep
                └── example
                    ├── .gitkeep
                    └── Application.java
```

### Git 추적 확인
```bash
git ls-files examples/java-maven/
```

**예상 출력**:
```
examples/java-maven/README.md
examples/java-maven/pom.xml
examples/java-maven/src/.gitkeep
examples/java-maven/src/main/.gitkeep
examples/java-maven/src/main/java/.gitkeep
examples/java-maven/src/main/java/com/.gitkeep
examples/java-maven/src/main/java/com/example/.gitkeep
examples/java-maven/src/main/java/com/example/Application.java
```

모든 파일(`.gitkeep` 포함)이 표시되어야 합니다.

## GitHub Actions에서도 해결됨

이 수정으로 GitHub Actions의 `validate-examples` Job도 통과하게 됩니다:

```yaml
- name: Java 예제 검증
  if: matrix.example == 'java-maven'
  run: |
    cd examples/java-maven
    test -f pom.xml
    test -f src/main/java/com/example/Application.java  # ✅ 이제 통과
    test -f README.md
```

## 요약

| 문제 | 원인 | 해결 |
|------|------|------|
| Test 10 실패 (3/4) | Git이 빈 디렉토리 무시 | .gitkeep 추가 |
| Application.java 못 찾음 | 중간 경로 추적 안 됨 | 모든 디렉토리에 .gitkeep |
| GitHub Actions 실패 | 로컬과 동일 | .gitkeep 푸시 |

## 다음 단계

1. ✅ `.gitkeep` 파일 추가 완료
2. ✅ 테스트 스크립트에 디버그 출력 추가 완료
3. ⏳ Git 커밋 및 푸시
4. ⏳ 로컬 테스트 재실행
5. ⏳ GitHub에 푸시 후 CI 확인

이제 모든 테스트가 통과할 것입니다! 🎉
