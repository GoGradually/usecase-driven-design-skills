# uc-agent — UseCase 설계 멀티 에이전트 시스템

Claude Agent SDK 기반의 멀티 에이전트 시스템으로, UseCase 주도 설계 스킬들을
**오케스트레이터-워커 패턴**으로 자동 조율합니다.

## 아키텍처

```
사용자 → Orchestrator Agent (코디네이터)
              ├── uc-new-project   (새 프로젝트 8단계 설계)
              ├── uc-add-feature   (기존 프로젝트에 기능 추가)
              ├── uc-review        (5관점 리뷰) ← 병렬 실행 가능
              ├── uc-merge         (메인 문서 병합)
              └── uc-deprecate     (UC 폐기/제거)
```

- **Orchestrator**: 사용자 요청을 분석하여 적절한 워커 에이전트를 선택하고 시퀀싱
- **Workers**: 각 SKILL.md를 시스템 프롬프트로 사용하여 파일 기반 산출물 생성

## 설치

```bash
# 개발 모드 설치
cd uc-agent
pip install -e ".[dev]"

# 또는 직접 설치
pip install -e .
```

**요구사항:**
- Python 3.10+
- `claude-agent-sdk` (자동 설치)
- Anthropic API 키 (`ANTHROPIC_API_KEY` 환경변수)

## 사용법

### 기본 사용 (인터랙티브 모드)

각 단계마다 사용자 확인을 받으며 진행합니다:

```bash
uc-agent "주문 관리 시스템 설계"
```

또는 `python -m uc_agent`로 실행:

```bash
python -m uc_agent "주문 관리 시스템 설계"
```

### 자동 파이프라인 모드

8단계 워크플로우를 자동으로 진행하고, 리뷰 → 병합까지 자동 처리합니다:

```bash
uc-agent --mode automated "주문 관리 시스템 설계"
```

자동 모드에서의 동작:
1. `uc-new-project` 에이전트가 8단계 step 파일 생성
2. `uc-review` 에이전트가 5관점 리뷰 수행
3. CRITICAL 이슈가 있으면 자동 수정 후 재리뷰
4. `uc-merge` 에이전트가 메인 설계서에 병합
5. CRITICAL 이슈가 2회 미해결 시에만 사용자에게 에스컬레이션

### 단일 스킬 실행

오케스트레이터 없이 특정 스킬만 직접 실행합니다:

```bash
# 리뷰만 실행
uc-agent --skill uc-review "docs/usecase/drafts/order/order-draft.md를 리뷰해주세요"

# 병합만 실행
uc-agent --skill uc-merge "order 초안을 메인 문서에 병합해주세요"

# 기능 추가
uc-agent --skill uc-add-feature "결제 기능을 추가해주세요"
```

### 병렬 리뷰

여러 초안을 동시에 리뷰합니다:

```bash
uc-agent --parallel-review \
  docs/usecase/drafts/order/order-draft.md \
  docs/usecase/drafts/payment/payment-draft.md
```

### 프로젝트 디렉토리 지정

```bash
uc-agent --cwd /path/to/my-project "회원 관리 시스템 설계"
```

### 모델 지정

```bash
# 오케스트레이터는 Opus, 워커는 Sonnet
uc-agent --model claude-opus-4-6 --worker-model claude-sonnet-4-6 "주문 관리 시스템 설계"
```

## 옵션 전체 목록

| 옵션 | 기본값 | 설명 |
|------|--------|------|
| `prompt` | (필수) | 설계 요청 텍스트 |
| `--mode` | `interactive` | `automated` 또는 `interactive` |
| `--cwd` | `.` | 프로젝트 루트 디렉토리 |
| `--skill` | — | 단일 스킬 직접 실행 |
| `--model` | — | 오케스트레이터 모델 |
| `--worker-model` | — | 워커 에이전트 모델 |
| `--max-turns` | `200` | 최대 에이전틱 턴 수 |
| `--skills-dir` | 자동 감지 | SKILL.md 디렉토리 경로 |
| `--parallel-review` | — | 병렬 리뷰할 draft 경로 목록 |

## 실행 모드 비교

| | Automated | Interactive |
|---|---|---|
| 사용자 확인 | CRITICAL 에스컬레이션 시에만 | 매 단계 |
| 파이프라인 | 자동 (초안→리뷰→병합) | 단계별 제안 |
| 적합한 상황 | 빠른 초안 생성 | 신중한 설계, 학습 |
| 소요 시간 | 짧음 | 사용자 응답에 따라 다름 |

## 산출물 구조

실행 후 프로젝트 디렉토리에 생성되는 파일:

```
docs/usecase/
├── [project]-usecase-design.md       ← 메인 통합 설계서
├── merge-report-[날짜].md            ← 병합 리포트
├── drafts/
│   └── [feature]/
│       ├── step1-usecases.md         ← 1단계: 유스케이스 목록
│       ├── step2-scenarios.md        ← 2단계: 시나리오
│       ├── step3-variables.md        ← 3단계: 변수 식별
│       ├── step4-domain-model.md     ← 4단계: 도메인 모델
│       ├── step5-state-model.md      ← 5단계: 상태 모델
│       ├── step6-system-boundary.md  ← 6단계: 시스템 경계
│       ├── step7-exceptions.md       ← 7단계: 예외 정리
│       ├── step8-conditions.md       ← 8단계: 사전/사후조건
│       ├── review-report.md          ← 리뷰 리포트
│       └── [feature]-draft.md        ← 통합 초안
└── deprecated/                        ← 폐기된 UC 백업
```

## 에스컬레이션 정책

자동 모드에서 사용자에게 에스컬레이션되는 경우:

| 상황 | 동작 |
|------|------|
| step 파일 검증 2회 실패 | 사용자에게 해당 step 확인 요청 |
| 리뷰 CRITICAL 수정 후에도 남음 | 사용자에게 이슈 목록 제시 |
| 도메인 모델 충돌 | 사용자가 병합 전략 결정 |
| 상태 모델 금지 전이 위반 | 사용자가 해결 방법 결정 |

## 개발

```bash
# 테스트 실행
pip install -e ".[dev]"
pytest tests/

# 타입 체크 (선택)
pip install mypy
mypy src/uc_agent/
```
