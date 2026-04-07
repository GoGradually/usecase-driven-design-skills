# uc-agent — UseCase 설계 멀티 에이전트 시스템

Claude Agent SDK 기반의 멀티 에이전트 시스템으로, UseCase 주도 설계 스킬들을
**오케스트레이터-워커 패턴**으로 자동 조율합니다.

## 아키텍처

```
사용자 → Orchestrator Agent (코디네이터)
              ├── uc-new-project   (새 프로젝트 8단계 설계)
              ├── uc-add-feature   (기존 프로젝트에 기능 추가)
              ├── critic           (즉각 CRITICAL 검사) ← Haiku
              ├── uc-review        (5관점 리뷰) ← 병렬 실행 가능
              ├── uc-merge         (메인 문서 병합)
              └── uc-deprecate     (UC 폐기/제거)
```

- **Orchestrator**: 적응형 라우팅으로 프로젝트 규모 분석 → 전략 선택 → 에이전트 시퀀싱
- **Workers**: 각 SKILL.md를 시스템 프롬프트로 사용, 스킬별 최적 모델 자동 배정
- **Critic**: 생성 직후 CRITICAL 이슈 사전 차단 (Haiku로 경량 실행)

## 설치

```bash
cd uc-agent
pip install -e ".[dev]"
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

### 자동 파이프라인 모드

8단계 워크플로우를 자동으로 진행합니다:

```bash
uc-agent --mode automated "주문 관리 시스템 설계"
```

자동 모드 파이프라인:
1. **생성**: `uc-new-project`가 8단계 step 파일 생성
2. **즉각 검사**: `critic`이 CRITICAL 이슈 사전 검사/수정
3. **리뷰**: `uc-review`가 5관점 리뷰 수행
4. **수정**: CRITICAL 이슈 자동 수정 후 재리뷰
5. **병합**: `uc-merge`가 메인 설계서에 병합
6. **피드백**: 리뷰 패턴을 수집하여 다음 생성에 반영

### 비용 티어

작업 난이도에 따라 모델을 자동 배정합니다:

```bash
# 저비용 (모든 워커 Haiku, 오케스트레이터 Sonnet)
uc-agent --cost-tier economy "간단한 할일 앱 설계"

# 균형 (기본값: 생성=Sonnet, 리뷰/분석=Opus)
uc-agent --cost-tier standard "주문 관리 시스템 설계"

# 최고 품질 (모든 에이전트 Opus)
uc-agent --cost-tier premium "이커머스 플랫폼 설계"
```

적응형 라우팅이 프로젝트 규모를 자동 판단하여 cost-tier를 추천합니다:
- **소규모** ("할일 앱", "메모 앱") → economy + 간소화 워크플로우
- **중규모** ("주문 관리 시스템") → standard
- **대규모** ("이커머스 플랫폼") → premium + 도메인 분할 전략

### 체크포인트/재개

중단된 작업을 이어서 진행합니다:

```bash
# step 4까지 완료 후 중단된 경우
uc-agent --resume docs/usecase/drafts/order/
# → step 5부터 자동 재개
```

### 단일 스킬 실행

```bash
uc-agent --skill uc-review "order-draft.md를 리뷰해주세요"
uc-agent --skill uc-merge "order 초안을 병합해주세요"
```

### 병렬 리뷰

```bash
uc-agent --parallel-review \
  docs/usecase/drafts/order/order-draft.md \
  docs/usecase/drafts/payment/payment-draft.md
```

### MCP 서버

다른 AI 도구에서 UseCase 설계 기능을 호출할 수 있습니다:

```bash
# MCP 서버 실행
uc-agent-mcp
```

Claude Code에서 사용:
```json
{
  "mcpServers": {
    "uc-design": {
      "command": "uc-agent-mcp"
    }
  }
}
```

제공 도구: `design_project`, `review_draft`, `merge_draft`, `review_drafts_parallel`

## 옵션 전체 목록

| 옵션 | 기본값 | 설명 |
|------|--------|------|
| `prompt` | (필수) | 설계 요청 텍스트 |
| `--mode` | `interactive` | `automated` 또는 `interactive` |
| `--cwd` | `.` | 프로젝트 루트 디렉토리 |
| `--skill` | — | 단일 스킬 직접 실행 |
| `--model` | — | 오케스트레이터 모델 |
| `--worker-model` | — | 워커 에이전트 모델 |
| `--cost-tier` | `standard` | 비용 티어 (`economy`, `standard`, `premium`) |
| `--resume` | — | 중단된 워크플로우 재개 (drafts 디렉토리) |
| `--max-turns` | `200` | 최대 에이전틱 턴 수 |
| `--skills-dir` | 자동 감지 | SKILL.md 디렉토리 경로 |
| `--parallel-review` | — | 병렬 리뷰할 draft 경로 목록 |

## 고급 기능

### 적응형 라우팅

사용자 요청에서 프로젝트 규모를 자동 분석하여 실행 전략을 결정합니다:

| 규모 | 판단 기준 | 워크플로우 | 비용 티어 | 병합 |
|------|----------|-----------|----------|------|
| 소규모 | "간단한", "할일" 등 | 간소화 (UC 3개 이하) | economy | 자동 |
| 중규모 | 일반 시스템 | 표준 8단계 | standard | 자동 |
| 대규모 | "플랫폼", 도메인 4개+ | 도메인 분할 → 병렬 | premium | 수동 |

### 피드백 루프

리뷰에서 반복 발견되는 패턴을 `docs/usecase/.feedback-history.json`에 축적합니다.
다음 설계 시 생성 에이전트의 프롬프트에 자동 주입되어 **같은 실수를 반복하지 않습니다**.

### 시맨틱 검증

regex 기반 구조 검증 외에, Haiku 모델을 사용한 의미적 검증을 지원합니다:
- 사용자 요구사항 대비 커버리지 점수 (0.0~1.0)
- 누락된 기능/시나리오 자동 식별

### 옵저버빌리티

파이프라인 실행 후 추적 리포트가 자동 생성됩니다:
- `.trace-{timestamp}.json` — 에이전트별 시간/비용/상태
- 터미널에 실행 요약 테이블 출력

## 산출물 구조

```
docs/usecase/
├── [project]-usecase-design.md       ← 메인 통합 설계서
├── merge-report-[날짜].md            ← 병합 리포트
├── .feedback-history.json            ← 피드백 히스토리
├── .trace-[timestamp].json           ← 실행 트레이스
├── drafts/
│   └── [feature]/
│       ├── .checkpoint.json          ← 체크포인트
│       ├── step1-usecases.md ~ step8-conditions.md
│       ├── review-report.md
│       └── [feature]-draft.md
└── deprecated/
```

## 에스컬레이션 정책

| 상황 | 동작 |
|------|------|
| step 파일 검증 2회 실패 | 사용자에게 해당 step 확인 요청 |
| 리뷰 CRITICAL 수정 후에도 남음 | 사용자에게 이슈 목록 제시 |
| 도메인 모델 충돌 | 사용자가 병합 전략 결정 |
| 대규모 프로젝트 병합 | 도메인 간 의존성 사용자 확인 |

## 개발

```bash
pip install -e ".[dev]"
pytest tests/
```
