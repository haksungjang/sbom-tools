# SBOM Tools - 빠른 시작 가이드

## 5분 안에 시작하기

### 1. 예제 실행 (가장 빠름)

```bash
# 저장소 클론
git clone https://github.com/sktelecom/sbom-tools.git
cd sbom-tools

# Java Maven 예제 실행
cd examples/java-maven
./run.sh

# 결과 확인
cat JavaMavenExample_1.0.0_bom.json | jq .
```

### 2. 자신의 프로젝트에서 사용

```bash
# 스크립트 다운로드
curl -O https://raw.githubusercontent.com/sktelecom/sbom-tools/main/scripts/scan-sbom.sh
chmod +x scan-sbom.sh

# 프로젝트에서 실행
cd /path/to/your/project
./scan-sbom.sh --project "MyApp" --version "1.0.0" --generate-only

# SBOM 생성 완료!
cat MyApp_1.0.0_bom.json | jq .
```

### 3. 테스트 실행

```bash
cd sbom-tools/tests
./test-scan.sh

# 모든 테스트가 통과하면:
# ✓ PASS: java
# ✓ PASS: python
# ✓ PASS: nodejs
```

## 다음 단계

- 상세 가이드: [README.ko.md](README.ko.md)
- 예제 활용: [docs/examples-guide.md](docs/examples-guide.md)
- 기여하기: [CONTRIBUTING.md](CONTRIBUTING.md)
- 아키텍처: [docs/architecture.md](docs/architecture.md)

## 학습 경로

1. 초보자
   - examples/java-maven → Python → Node.js
   - 각 README.md 읽기
   - run.sh 실행해보기

2. 개발자
   - CONTRIBUTING.md 읽기
   - tests/test-scan.sh 실행
   - 새 예제 추가해보기

3. 기여자
   - docs/contributing-guide.md 읽기
   - 새 패키지 매니저 지원 추가
   - Pull Request 생성

## 문제가 있나요?

```bash
# 디버그 모드로 실행
DEBUG=true ./scan-sbom.sh --project "Test" --version "1.0" --generate-only

# 테스트 상세 모드
./test-scan.sh -v

# Docker 확인
docker --version
docker pull ghcr.io/sktelecom/sbom-scanner:latest
```

이슈가 계속되면 GitHub Issues에 리포트해주세요!
