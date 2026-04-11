---
name: ood-add-feature
description: 기존 OOD 설계서가 있는 프로젝트에 새로운 기능의 OOD 초안을 추가한다. 기존 OOD(아키텍처·계층·클래스·인터페이스)와 신규 OOA(유스케이스·도메인 모델·상태 모델)를 동시에 분석하여, 기존 클래스/패키지를 재사용하면서 일관된 설계를 작성한다. 6단계 워크플로우(아키텍처 → Use Case Realization → 책임 할당 → 디자인 패턴 → 설계 클래스 다이어그램 → 영속성·횡단 관심사)를 단계별 확인을 받으며 진행한다. 'OOD 기능 추가', '설계에 추가', '클래스 추가', '기능 설계 확장' 등의 요청에 사용한다. 기존 OOD가 없는 경우에는 ood-new-project 스킬을 사용한다.
---

# 기존 OOD에 새 기능 설계 초안 만들기

## 개요

이미 OOD 설계가 있는 프로젝트에 새로운 기능의 OOD를 추가한다.
기존 OOD 산출물과 신규 OOA 산출물을 **먼저 분석**한 뒤, 6단계 OOD 워크플로우를 진행한다.
**기존 클래스/패키지/인터페이스의 재사용**과 **계층 의존 규칙 일관성**이 핵심이다.

이 스킬은 ood-new-project의 확장이다. 6단계 워크플로우와 단계별 산출물 형식은 ood-new-project와 동일하며, 이 문서는 차이점만 기술한다. 공통 사항은 ood-new-project의 SKILL.md를 참조한다.

---

## 의존성 (필수 검증)

이 스킬은 **두 가지 입력**이 모두 존재해야 동작한다:

1. **기존 OOD 산출물** — 다음 중 하나:
   - `docs/design/[project-name]-design.md` (메인 설계서)
   - `docs/design/drafts/[기존-feature]/[기존-feature]-design-draft.md` (이전 기능 통합 초안)

2. **신규 기능의 OOA 산출물** — 다음 중 하나:
   - `docs/usecase/[project-name]-usecase-design.md`에 신규 UC가 병합되어 있음
   - `docs/usecase/drafts/[새-feature]/[새-feature]-draft.md` (신규 기능의 OOA 초안)

둘 중 하나라도 없으면 즉시 실행을 중단하고 다음을 안내한다:

```
ood-add-feature를 사용하려면 다음 두 가지가 모두 필요합니다:

1. 기존 OOD: docs/design/[project]-design.md 또는 docs/design/drafts/[기존-feature]/...
   → 없으면 ood-new-project로 첫 OOD를 먼저 작성하세요.

2. 신규 기능의 OOA: docs/usecase/drafts/[새-feature]/[새-feature]-draft.md
   → 없으면 uc-add-feature로 OOA부터 작성하세요.
```

---

## 파일 기반 출력 규칙

ood-new-project와 동일하다. 모든 산출물은 채팅이 아닌 파일에 기록한다. 채팅에는 안내와 변경 요약(예: "기존 클래스 3개 재사용, 신규 클래스 4개 추가")만 표시한다.

---

## 디렉토리 구조

```
[project-root]/
└── docs/
    ├── usecase/                                    ← OOA
    │   └── drafts/[새-feature]/
    │       └── [새-feature]-draft.md               ← 신규 OOA 입력
    │
    └── design/                                     ← OOD
        ├── [project-name]-design.md                ← 기존 메인 (있으면 참조)
        ├── drafts/
        │   ├── [기존-feature]/                      ← 기존 OOD 초안 (참조)
        │   │   └── [기존-feature]-design-draft.md
        │   └── [새-feature]/                        ← 이 스킬이 생성
        │       ├── step0-existing-analysis.md       ← 기존 OOD/신규 OOA 분석
        │       ├── step1-architecture.md
        │       ├── step2-interactions.md
        │       ├── step3-responsibilities.md
        │       ├── step4-design-patterns.md
        │       ├── step5-class-diagram.md
        │       ├── step6-cross-cutting.md
        │       └── [새-feature]-design-draft.md
        └── deprecated/
```

---

## 시작 절차

1. **두 입력 검증**:
   ```bash
   ls docs/design/
   ls docs/design/drafts/
   ls docs/usecase/drafts/
   ```
2. 사용자에게 다음을 확인:
   - 어떤 기존 OOD를 참조할지 (메인 설계서 / 특정 기존 feature 초안)
   - 어떤 신규 OOA를 입력으로 사용할지
   - 새 기능의 feature 이름 (보통 신규 OOA의 feature 이름과 동일)
3. 디렉토리 생성:
   ```bash
   mkdir -p docs/design/drafts/[새-feature]
   ```
4. **step0**부터 시작 (ood-new-project와 다른 점).

---

## Step 0: 기존 OOD + 신규 OOA 분석

**파일:** `docs/design/drafts/[새-feature]/step0-existing-analysis.md`

기존 OOD 산출물과 신규 OOA 산출물을 동시에 읽고, 신규 기능이 기존 설계 위에서 어떻게 자리 잡을지 예비 분석한다. 이 단계는 step1~6 전체의 기준점이 된다.

```markdown
# Step 0: 기존 OOD + 신규 OOA 분석

> 프로젝트: [project-name]
> 새 기능: [feature-name]
> 분석일: [날짜]
> 기존 OOD: [경로]
> 신규 OOA: [경로]

## 1. 기존 아키텍처 + 계층 요약

| 항목 | 값 |
|------|------|
| 아키텍처 스타일 | Hexagonal |
| 계층 | presentation, application, domain, infrastructure |
| 의존 방향 규칙 | presentation → application → domain ← infrastructure |

## 2. 기존 클래스 목록

| 클래스 | 패키지 | 스테레오타입 | 비고 |
|--------|------|------------|------|
| Order | domain | «entity», «aggregate root» | |
| OrderItem | domain | «entity» | Order의 합성 |
| Customer | domain | «entity», «aggregate root» | |
| OrderApplicationService | application | «service», «use case controller» | UC-01, UC-02 |
| OrderRepository | domain | «interface» | |
| JpaOrderRepository | infrastructure | «adapter» | |
| PaymentGateway | domain | «interface» | |
| StripePaymentAdapter | infrastructure | «adapter» | |

## 3. 기존 인터페이스(포트) 목록

| 인터페이스 | 패키지 | 메서드 |
|-----------|------|--------|
| OrderRepository | domain | save, findById, findByCustomer |
| PaymentGateway | domain | charge, refund |

## 4. 기존 디자인 패턴 적용

| 패턴 | 참여 클래스 | 적용 이유 |
|------|-----------|---------|
| State | Order, OrderState, CreatedState/PaidState/... | 주문 상태 분기 |
| Strategy | PaymentService, PaymentStrategy | 결제 수단 다양성 |

## 5. 신규 OOA 요약

| 항목 | 내용 |
|------|------|
| 신규 UC | UC-06 환불 요청, UC-07 환불 승인 |
| 신규 액터 | (없음, 기존 액터 재사용) |
| 신규 엔티티 | Refund |
| 확장 엔티티 | Order에 REFUND_REQUESTED, REFUNDED 상태 추가 |
| 신규 도메인 규칙 | 환불은 결제 완료 후 7일 이내 |

## 6. 영향 분석 (기존 OOD에 미치는 영향)

| 기존 요소 | 영향 종류 | 영향 내용 |
|---------|---------|---------|
| Order 클래스 | 확장 | requestRefund() 메서드 추가, REFUND_REQUESTED/REFUNDED 상태 추가 |
| OrderState 계층 | 확장 | RefundRequestedState, RefundedState 클래스 추가 |
| OrderApplicationService | 확장 또는 분리 | UC-06/07 추가. 6개 UC 누적 → Bloated Controller 검토 |
| PaymentGateway | 재사용 | 기존 refund() 메서드 활용 |
| OrderRepository | 재사용 | 변경 없음 |

## 7. 신규 클래스 후보 (예비)

| 클래스 (예비) | 패키지 | 스테레오타입 | 역할 |
|------------|------|------------|------|
| Refund | domain | «entity», «aggregate root» | 환불 정보 |
| RefundApplicationService | application | «service» | UC-06/07 (분리 권장) |
| RefundRepository | domain | «interface» | 환불 영속성 |
| JpaRefundRepository | infrastructure | «adapter» | RefundRepository 구현 |
| RefundPolicy | domain | «service» | 7일 규칙 검증 |

## 8. 패키지 배치 결정

| 신규 클래스 | 배치 패키지 | 근거 |
|----------|----------|------|
| Refund | domain | 도메인 엔티티 |
| RefundApplicationService | application | UC controller |
| RefundRepository | domain | 인터페이스 (DIP) |
| JpaRefundRepository | infrastructure | 구현 (DIP) |

기존 패키지 구조를 그대로 따르며, **새 패키지를 만들 필요 없음**.

## 9. 재사용/확장/신규 결정 요약

| 분류 | 항목 | 비고 |
|------|------|------|
| 재사용 (변경 없음) | Customer, OrderRepository, PaymentGateway, OrderItem | |
| 확장 | Order, OrderState 계층, OrderApplicationService(?) | |
| 신규 | Refund, RefundApplicationService, RefundPolicy, RefundRepository, JpaRefundRepository | |
```

**→ 파일 저장 후 사용자에게 분석 결과를 확인받고, 영향 범위·재사용 결정·신규 클래스 후보에 대해 피드백을 받는다. 동의가 되면 1단계로 진행.**

---

## Step 1~6: 6단계 워크플로우

ood-new-project의 step1~6을 순차 진행한다. 단, 다음 **add-feature 전용 규칙**을 적용한다:

### 공통 규칙 — 기존/신규 구분 표기

모든 step의 표와 다이어그램에서 기존/신규를 구분한다:

| 표기 | 의미 | 예 |
|------|------|---|
| `%% NEW` | 신규로 추가된 클래스/인터페이스/메서드 | `Refund "Refund" %% NEW` |
| `%% EXTENDED` | 기존 클래스에 메서드/속성/상태가 추가됨 | `Order "Order" %% EXTENDED` |
| (주석 없음) | 변경 없는 기존 클래스 (참조용) | `Customer` |

표에서는 "구분" 컬럼을 추가하여 **기존 / 확장 / 신규** 3분류로 표기한다.

### Step 1: 아키텍처 + 계층 분해

- 기존 아키텍처 스타일과 패키지 구조를 그대로 재사용한다 (변경 금지를 권장).
- step0의 "기존 아키텍처 + 계층 요약"을 그대로 옮기고, **새 패키지를 만든 경우에만** 추가한다.
- 신규 클래스의 패키지 배치는 step0의 "패키지 배치 결정"을 인용한다.
- BCE → 계층 매핑 표는 신규 BCE 항목만 추가 (기존 표 전체를 다시 그릴 필요 없음).
- 계층 의존도 다이어그램은 기존 다이어그램을 인용하고, **변경이 있는 경우에만** 다시 그린다.

### Step 2: Use Case Realization

- 신규 UC만 다룬다 (기존 UC는 다시 그리지 않는다).
- participant 목록에 **기존 클래스를 재사용**하고, 새 메시지가 추가될 때 `Note over` 등으로 표시.
- 새 participant(신규 클래스)는 다이어그램에 `%% NEW` 주석.

### Step 3: GRASP 책임 할당

- 책임 카탈로그는 **신규 책임만** 나열한다.
- GRASP 할당 표에서 "할당 클래스" 컬럼이 기존 클래스인 경우 `(기존)` 표기를 추가한다.
- Controller 목록 갱신 시, **기존 Controller가 5개 이상 UC를 담당하게 되면 분리를 권고**한다 (Bloated Controller 경고).

### Step 4: 디자인 패턴 적용

- 기존 패턴(Step0의 "기존 디자인 패턴 적용") 안에서 신규 기능이 풀리면, **새 패턴 도입 없이** "기존 패턴 확장"으로 표기 (예: "기존 State 패턴에 RefundRequestedState 추가").
- 신규 패턴 도입은 step0에서 이미 식별된 문제 상황에 한정하고, 반증 표를 반드시 채운다.

### Step 5: 설계 클래스 다이어그램 (DCD)

- **기존 클래스**: 회색 또는 옅은 색으로 배경 표시 (가능한 경우). Mermaid에서 `style 클래스명 fill:#f0f0f0,stroke:#999`.
- **확장 클래스 (`%% EXTENDED`)**: 추가된 메서드·속성·상태에 `+추가` 표시. 기존 메서드는 그대로 유지.
- **신규 클래스 (`%% NEW`)**: 강조 색 또는 굵은 테두리. 모든 클래스는 ood-new-project의 규칙에 따라 가시성·타입·시그니처·스테레오타입·패키지·`%% traced-from:` 주석을 모두 갖는다.

확장 클래스의 추적 주석은 신규 OOA 요소까지 포함한다:
```
%% traced-from: OOA Order entity, UC-01 (기존), UC-06 (신규), Step3 R01-R03 (기존) + R10 (신규)
```

### Step 6: 영속성 + 횡단 관심사

- Repository 목록에 신규 Repository만 추가.
- 트랜잭션 경계 표에 신규 UC만 추가.
- 에러 정책 표에 신규 OOA 예외만 추가.
- **상태 모델 불허 전이**가 신규 상태 추가로 인해 변경되었는지 확인 (예: REFUNDED → CONFIRMED 같은 새 불허 전이).

---

## 최종 통합

ood-new-project와 동일한 형식으로 통합 초안 파일을 생성한다:

**파일:** `docs/design/drafts/[새-feature]/[새-feature]-design-draft.md`

차이점:
- 헤더에 "기존 OOD 위에 추가된 기능"임을 명시
- **변경 요약 섹션**을 OOA → OOD 추적성 매트릭스 바로 다음에 추가:

```markdown
## 변경 요약

| 분류 | 개수 | 항목 |
|------|------|------|
| 재사용 (변경 없음) | 4 | Customer, OrderRepository, PaymentGateway, OrderItem |
| 확장 | 3 | Order(상태 추가, 메서드 추가), OrderState 계층, OrderApplicationService(UC 추가) |
| 신규 | 5 | Refund, RefundApplicationService, RefundPolicy, RefundRepository, JpaRefundRepository |
```

통합 완료 후 사용자에게 다음을 제안한다:
- `ood-review`로 신규 OOD 초안 리뷰 (특히 OOA 정합성과 기존 OOD와의 일관성 검토)
