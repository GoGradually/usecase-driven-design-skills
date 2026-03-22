# UseCase 설계 스킬 사용 가이드

> 버전: v2 (파일 기반 출력)
> 대상 환경: Claude Code
> 스킬 수: 6개

---

## 목차

1. [개요](#1-개요)
2. [설치](#2-설치)
3. [스킬 구성 한눈에 보기](#3-스킬-구성-한눈에-보기)
4. [워크플로우 흐름도](#4-워크플로우-흐름도)
5. [스킬별 사용법](#5-스킬별-사용법)
    - [uc-new-project](#51-uc-new-project)
    - [uc-add-feature](#52-uc-add-feature)
    - [uc-review](#53-uc-review)
    - [uc-merge](#54-uc-merge)
    - [uc-deprecate](#55-uc-deprecate)
    - [usecase-driven-design](#56-usecase-driven-design)
6. [산출물 디렉토리 구조](#6-산출물-디렉토리-구조)
7. [실전 시나리오별 가이드](#7-실전-시나리오별-가이드)
8. [파일 상태 관리](#8-파일-상태-관리)
9. [FAQ](#9-faq)

---

## 1. 개요

이 스킬 셋은 **유스케이스 주도 설계(Use-Case Driven Design)** 를 체계적으로 수행하기 위한 Claude Code 전용 도구입니다.

### 핵심 특징

**파일 기반 출력** — 모든 산출물은 채팅이 아닌 마크다운 파일에 기록됩니다. 채팅에는 파일 경로와 간략한 안내만 표시되며, 실제 내용은 파일을 열어서 확인합니다. 이를 통해 다음과 같은 이점을 얻습니다:

- 긴 채팅 히스토리를 스크롤하며 내용을 찾을 필요가 없음
- 단계별 파일로 분리되어 특정 단계만 빠르게 찾아볼 수 있음
- Git 등 버전 관리 시스템과 자연스럽게 연동
- 수정 시 파일을 직접 편집하므로 변경 이력이 명확

### 스킬 간 관계

```
새 프로젝트 시작          기존 프로젝트에 기능 추가
       │                         │
 uc-new-project            uc-add-feature
       │                         │
       └──────────┬──────────────┘
                  │
              uc-review ← 리뷰 (선택)
                  │
              uc-merge ← 메인 문서로 통합
                  │
             uc-deprecate ← 기능 폐기/제거 (필요 시)
```

`usecase-driven-design`은 위 워크플로우의 경량 버전(6단계)으로, 초안/메인 문서 분리 없이 바로 설계서를 만들 때 사용합니다.

---

## 2. 설치

스킬 폴더를 Claude Code의 사용자 스킬 디렉토리에 복사합니다.

```bash
# 스킬 디렉토리 위치 (환경에 따라 다를 수 있음)
SKILL_DIR="$HOME/.claude/skills/user"

# 기존 스킬 백업 (이미 있는 경우)
for skill in uc-new-project uc-add-feature uc-review uc-merge uc-deprecate usecase-driven-design; do
  [ -d "$SKILL_DIR/$skill" ] && cp -r "$SKILL_DIR/$skill" "$SKILL_DIR/${skill}.bak"
done

# 새 스킬 복사
cp -r skills/uc-new-project "$SKILL_DIR/"
cp -r skills/uc-add-feature "$SKILL_DIR/"
cp -r skills/uc-review "$SKILL_DIR/"
cp -r skills/uc-merge "$SKILL_DIR/"
cp -r skills/uc-deprecate "$SKILL_DIR/"
cp -r skills/usecase-driven-design "$SKILL_DIR/"
```

---

## 3. 스킬 구성 한눈에 보기

| 스킬 | 용도 | 트리거 키워드 | 단계 | 주요 산출물 |
|------|------|-------------|------|-----------|
| `uc-new-project` | 새 프로젝트 UC 설계 | "새 프로젝트", "프로젝트 시작" | 7단계 | `step1~7.md` → 통합 초안 |
| `uc-add-feature` | 기존 프로젝트에 기능 추가 | "기능 추가", "새 기능 UseCase" | 7단계 + step0 | `step0~7.md` → 통합 초안 |
| `uc-review` | UC 문서 리뷰 | "리뷰", "검토", "초안 확인" | 5개 관점 | `review-report.md` |
| `uc-merge` | 초안을 메인 문서에 병합 | "병합", "머지", "merge" | 2개 시나리오 | 메인 설계서 + 병합 리포트 |
| `uc-deprecate` | UC 폐기/제거 | "폐기", "deprecate", "제거" | 6개 분석 + 실행 | 영향 분석 + 결과 리포트 |
| `usecase-driven-design` | 경량 UC 설계 | `/usecase-driven-design` | 6단계 | `step1~6.md` → 통합 설계서 |

---

## 4. 워크플로우 흐름도

### 일반적인 프로젝트 흐름

```
1. 프로젝트 시작
   └─→ uc-new-project (7단계 → 초안 생성)

2. 초안 리뷰 (권장)
   └─→ uc-review (리뷰 리포트 → 수정 반영)

3. 메인 문서 생성
   └─→ uc-merge (초안 → 메인 설계서)

4. 기능 추가 (반복)
   └─→ uc-add-feature (7단계 → 새 초안)
       └─→ uc-review (리뷰)
           └─→ uc-merge (메인에 병합)

5. 기능 폐기 (필요 시)
   └─→ uc-deprecate (영향 분석 → 실행)
```

### 간단한 설계

규모가 작거나 빠르게 진행할 때는 `usecase-driven-design`만 사용합니다:

```
usecase-driven-design (6단계 → 바로 설계서)
```

---

## 5. 스킬별 사용법

### 5.1 uc-new-project

새로운 프로젝트의 UseCase 설계를 처음부터 시작합니다.

#### 호출 예시

```
"주문 관리 시스템 프로젝트를 새로 시작하려고 해. UseCase를 설계해줘."
"새 프로젝트 이름은 delivery-app이야. 배달 앱의 유스케이스를 만들어줘."
```

#### 진행 흐름

```
사용자: 프로젝트 설명
    ↓
Claude: 디렉토리 생성 + 1단계 작성 → step1-usecases.md 저장
    ↓
사용자: 파일 확인 → "OK" 또는 "수정해줘"
    ↓
Claude: (수정 시 파일 편집) → 2단계 작성 → step2-scenarios.md 저장
    ↓
  ... (3~7단계 반복) ...
    ↓
Claude: 7단계 완료 → [feature]-draft.md 통합본 생성
```

#### 생성되는 파일

```
docs/usecase/drafts/[feature-name]/
├── step1-usecases.md        ← 유스케이스 목록 + 다이어그램
├── step2-scenarios.md        ← 시나리오 + 시퀀스 다이어그램
├── step3-variables.md        ← 독립변수/상수/종속변수 + 관계도
├── step4-domain-model.md     ← 엔티티, 관계, 규칙 + 클래스 다이어그램
├── step5-system-boundary.md  ← 외부/내부 분리 + 경계 다이어그램
├── step6-exceptions.md       ← 예외 정리
├── step7-conditions.md       ← 사전/사후조건
└── [feature-name]-draft.md   ← 최종 통합본
```

#### 단계별 확인 포인트

| 단계 | 확인할 내용 |
|------|-----------|
| 1단계 | UC 식별이 빠짐없는지, 크기가 적절한지 |
| 2단계 | 기본 흐름이 자연스러운지, 대안 흐름이 충분한지 |
| 3단계 | 변수 분류가 타당한지, 종속변수의 결정 요인이 맞는지 |
| 4단계 | 엔티티가 누락 없는지, 관계가 맞는지 |
| 5단계 | 내/외부 분리가 올바른지 |
| 6단계 | 예외가 빠짐없는지, 대응이 구체적인지 |
| 7단계 | 조건이 검증 가능한 형태인지 |

---

### 5.2 uc-add-feature

기존 프로젝트에 새로운 기능의 UseCase를 추가합니다.

#### 호출 예시

```
"기존 주문 시스템에 환불 기능을 추가하고 싶어."
"delivery-app 프로젝트에 리뷰/평점 기능 UseCase를 만들어줘."
```

#### 전제 조건

`docs/usecase/` 디렉토리가 이미 존재해야 합니다. 없으면 `uc-new-project`를 먼저 사용하세요.

#### 진행 흐름

```
Claude: 기존 문서 분석 → step0-existing-analysis.md 저장
    ↓
사용자: 분석 결과 확인 + 새 기능 설명
    ↓
Claude: 1~7단계 진행 (uc-new-project와 동일, ID는 기존 이어서)
    ↓
Claude: 통합본 생성
```

#### uc-new-project와의 차이점

| 항목 | uc-new-project | uc-add-feature |
|------|---------------|----------------|
| step0 | 없음 | 기존 문서 분석 파일 생성 |
| UC ID | UC-01부터 시작 | 기존 마지막 ID 다음부터 |
| 도메인 모델 | 새로 설계 | 기존 모델 확장 (기존/신규 구분) |
| 액터 | 새로 정의 | 기존 재사용 + 필요 시 추가 |
| 다이어그램 | 독립적 | 기존 노드를 포함하여 맥락 표현 |

---

### 5.3 uc-review

UseCase 문서를 5개 관점에서 체계적으로 리뷰합니다.

#### 호출 예시

```
"환불 기능 초안을 리뷰해줘."
"메인 설계서를 전체 검토해줘."
"도메인 모델만 집중적으로 봐줘."
```

#### 리뷰 5개 관점

| 관점 | 검토 초점 |
|------|----------|
| **완전성** | 7단계 모두 있는지, 빠진 UC/다이어그램 없는지 |
| **일관성** | ID 연속성, 용어 통일, 다이어그램↔표 일치 |
| **품질** | 시나리오 구체성, 변수 분류 타당성, 예외 대응 |
| **구조적 적절성** | UC 크기, 의존성 방향, 관계 정합성 |
| **기존 문서 정합성** | ID 충돌, 엔티티 충돌, 규칙 모순 (기존 문서 있을 때만) |

#### 생성되는 파일

```
docs/usecase/drafts/[feature]/review-report.md
```

#### 리뷰 후 선택지

리뷰 리포트를 확인한 뒤 세 가지 중 선택합니다:

1. **"전부 수정해줘"** → CRITICAL/WARNING 이슈를 원본 파일에 반영
2. **"확인만 할게"** → 리포트만 참고, 나중에 직접 수정
3. **"이것만 수정해줘"** → 특정 이슈만 선택하여 수정

---

### 5.4 uc-merge

하나 이상의 초안을 메인 설계서에 병합합니다.

#### 호출 예시

```
"환불 기능 초안을 메인 문서에 병합해줘."
"drafts 폴더에 있는 초안 전부 머지해줘."
```

#### 두 가지 시나리오

**시나리오 A — 메인 문서가 없을 때 (최초 병합)**
- 초안 내용을 메인 문서 형식으로 재구성
- UC ID를 UC-01부터 순서대로 재정렬

**시나리오 B — 메인 문서가 있을 때 (추가 병합)**
- 기존 메인 문서에 새 초안 내용을 추가
- ID를 기존 범위 다음부터 재부여

#### 생성/갱신되는 파일

```
docs/usecase/[project-name]-usecase-design.md   ← 메인 설계서
docs/usecase/merge-report-[날짜].md              ← 병합 리포트
```

#### 병합 시 자동 처리 사항

- UC ID 재정렬 (문서 전체에서 참조 갱신)
- 변수 식별 통합 (시나리오 근거, 결정 요인 ID 갱신)
- 도메인 모델 통합 (엔티티 합산, 중복 관계 제거)
- 용어 통일 (메인 문서 기준)
- Mermaid 다이어그램 전체 재생성

---

### 5.5 uc-deprecate

기존 UseCase를 폐기하거나 제거합니다.

#### 호출 예시

```
"UC-03 주문 취소 기능을 폐기해줘."
"환불 처리 UC를 완전히 제거해줘."
```

#### 두 가지 모드

| 모드 | 설명 | 사용 시기 |
|------|------|----------|
| **소프트 폐기** | `[DEPRECATED]` 마킹, 내용은 유지 | 이력 보존, 재활용 가능성 |
| **하드 제거** | 문서에서 완전 삭제 (백업 생성) | 더 이상 불필요 |

#### 진행 흐름

```
Claude: 대상 UC 분석 → impact-analysis-[UC-ID].md 저장
    ↓
사용자: 영향 분석 확인 + CRITICAL 해결 방안 논의
    ↓
사용자: 소프트 폐기 / 하드 제거 선택
    ↓
Claude: 실행 → 메인 문서 갱신 + deprecation-report 저장
```

#### 영향 분석 6개 관점

| 분석 | 확인 내용 |
|------|----------|
| UC 의존성 | 다른 UC가 이 UC를 참조하는 곳 |
| 변수 연쇄 | 종속변수가 다른 UC의 입력이 되는 경우 |
| 도메인 모델 | 이 UC 전용 엔티티 vs 공유 엔티티 |
| 시스템 경계 | 고아 액터, 트리거 소멸 |
| 예외/조건 | 삭제 대상 |
| Mermaid | 갱신이 필요한 다이어그램 |

#### 생성되는 파일

```
docs/usecase/impact-analysis-[UC-ID].md           ← 영향 분석 리포트
docs/usecase/deprecation-report-[날짜].md          ← 실행 결과 리포트
docs/usecase/deprecated/[UC-ID]-[name]-deprecated.md  ← 백업 (하드 제거 시)
```

---

### 5.6 usecase-driven-design

경량화된 유스케이스 설계 워크플로우입니다. 초안/메인 분리 없이 바로 설계서를 만듭니다.

#### 호출 예시

```
"/usecase-driven-design"
"간단하게 유스케이스 설계를 진행하고 싶어."
```

#### uc-new-project와의 차이

| 항목 | usecase-driven-design | uc-new-project |
|------|----------------------|----------------|
| 단계 수 | 6단계 | 7단계 (변수 식별 포함) |
| 변수 식별 | 없음 | 3단계에서 수행 |
| Mermaid | 없음 | 모든 단계에 포함 |
| 산출물 | 바로 설계서 | 초안 → merge로 설계서 |
| 디렉토리 | `docs/usecase/step*.md` | `docs/usecase/drafts/[feature]/step*.md` |
| 적합한 상황 | 소규모, 빠른 진행 | 중대규모, 체계적 관리 |

---

## 6. 산출물 디렉토리 구조

프로젝트가 성숙해지면 다음과 같은 구조가 됩니다:

```
[project-root]/
└── docs/
    └── usecase/
        │
        ├── my-project-usecase-design.md     ← 메인 통합 설계서
        │
        ├── merge-report-2026-03-22.md       ← 병합 리포트들
        ├── merge-report-2026-04-10.md
        │
        ├── impact-analysis-UC-05.md         ← 영향 분석 리포트
        ├── deprecation-report-2026-04-15.md ← 폐기 결과 리포트
        │
        ├── drafts/
        │   ├── order/                        ← 1차 기능 초안
        │   │   ├── step0-existing-analysis.md  (add-feature만)
        │   │   ├── step1-usecases.md
        │   │   ├── step2-scenarios.md
        │   │   ├── step3-variables.md
        │   │   ├── step4-domain-model.md
        │   │   ├── step5-system-boundary.md
        │   │   ├── step6-exceptions.md
        │   │   ├── step7-conditions.md
        │   │   ├── review-report.md
        │   │   └── order-draft.md
        │   │
        │   └── refund/                       ← 2차 기능 초안
        │       ├── step0-existing-analysis.md
        │       ├── step1-usecases.md
        │       ├── ...
        │       ├── review-report.md
        │       └── refund-draft.md
        │
        └── deprecated/                       ← 폐기 백업
            └── UC-05-cancel-deprecated.md
```

---

## 7. 실전 시나리오별 가이드

### 시나리오 A: 프로젝트를 처음 시작할 때

```
1. "주문 관리 시스템 프로젝트를 시작하자. 유스케이스를 설계해줘."
   → uc-new-project 실행

2. 7단계 완료 후:
   "초안 리뷰해줘."
   → uc-review 실행

3. 리뷰 이슈 수정 후:
   "메인 문서로 병합해줘."
   → uc-merge 실행
```

### 시나리오 B: 기존 프로젝트에 기능을 추가할 때

```
1. "환불 기능을 추가하고 싶어."
   → uc-add-feature 실행

2. 7단계 완료 후:
   "리뷰 부탁해."
   → uc-review 실행

3. "메인에 머지해줘."
   → uc-merge 실행
```

### 시나리오 C: 기능을 폐기할 때

```
1. "UC-03 주문 취소 기능을 제거하고 싶어."
   → uc-deprecate 실행 (영향 분석)

2. 영향 분석 확인 후:
   "CRITICAL 항목은 UC-05 시나리오를 수정하는 걸로 하자. 하드 제거해줘."
   → 실행 진행
```

### 시나리오 D: 빠르게 설계만 하고 싶을 때

```
1. "/usecase-driven-design"
   → usecase-driven-design 실행 (6단계)
```

---

## 8. 파일 상태 관리

모든 단계별 파일은 헤더에 상태를 표시합니다:

| 상태 | 의미 | 다음 행동 |
|------|------|----------|
| `✏️ 작성중` | 방금 생성됨, 확인 대기 | 파일을 열어 내용 확인 |
| `✅ 확인완료` | 사용자가 승인함 | 다음 단계로 진행 가능 |

초안 파일의 상태:

| 상태 | 의미 |
|------|------|
| `초안 (draft)` | 작성 완료, 리뷰/병합 가능 |
| `병합 완료 (merged) — [날짜]` | 메인 문서에 병합됨 |

---

## 9. FAQ

### Q: 특정 단계를 건너뛸 수 있나요?

아니요. 각 단계는 이전 단계의 산출물에 의존하므로 순서대로 진행해야 합니다. 다만, 특정 단계의 내용이 간단하면 빠르게 확인하고 넘어갈 수 있습니다.

### Q: 단계별 파일을 직접 수정해도 되나요?

네. 파일을 직접 편집한 뒤 Claude에게 "step2 수정했어, 확인해줘"라고 말하면 됩니다. Claude가 파일을 읽고 문제가 없는지 확인해줍니다.

### Q: usecase-driven-design과 uc-new-project 중 어떤 걸 써야 하나요?

- **소규모 프로젝트**, 빠른 프로토타이핑 → `usecase-driven-design` (6단계, Mermaid 없음)
- **중대규모 프로젝트**, 지속적 기능 추가 예정 → `uc-new-project` (7단계, 초안/메인 분리, Mermaid 포함)

### Q: 리뷰 없이 바로 병합해도 되나요?

가능합니다. `uc-merge`를 실행하면 리뷰를 권장하지만, 사용자가 원하면 바로 진행합니다.

### Q: 병합 후 초안 파일은 삭제해도 되나요?

삭제해도 동작에 문제는 없지만, 이력 추적을 위해 보존하는 것을 권장합니다. 병합된 초안은 상태가 `merged`로 변경되어 구분이 됩니다.

### Q: 한 번에 여러 기능의 초안을 만들 수 있나요?

네. `uc-add-feature`를 여러 번 실행하여 각각의 초안을 만든 뒤, `uc-merge`로 한 번에 병합할 수 있습니다.

### Q: 폐기한 UC를 되살릴 수 있나요?

- **소프트 폐기**한 경우: `[DEPRECATED]` 마킹을 제거하면 됩니다.
- **하드 제거**한 경우: `deprecated/` 폴더의 백업 파일을 참고하여 다시 추가합니다. `uc-add-feature`로 재추가하는 것을 권장합니다.