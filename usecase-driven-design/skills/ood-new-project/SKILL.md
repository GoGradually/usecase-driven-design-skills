---
name: ood-new-project
description: OOA(유스케이스 주도 분석)가 완료된 프로젝트에 객체지향 설계(OOD) 초안을 처음 만든다. 6단계 워크플로우(아키텍처·계층 분해 → Use Case Realization → GRASP 책임 할당 → GoF 디자인 패턴 → 설계 클래스 다이어그램(DCD) → 영속성·횡단 관심사)를 단계별 확인을 받으며 진행한다. 각 단계 산출물은 개별 마크다운 파일에 기록하고, 완료 후 하나의 설계 초안 파일로 통합한다. 'OOD 시작', '설계 초안', '클래스 설계', '아키텍처 설계', 'design 만들기' 등의 요청에 사용한다. OOA 산출물(docs/usecase/*-usecase-design.md 또는 docs/usecase/drafts/[feature]/[feature]-draft.md)이 반드시 존재해야 한다. 기존 OOD 문서에 신규 기능을 추가하는 경우에는 ood-add-feature 스킬을 사용한다.
---

# 새로운 OOD(객체지향 설계) 초안 만들기

## 개요

OOA가 완료된 프로젝트의 객체지향 설계(Object-Oriented Design)를 처음부터 시작한다.
**6단계 워크플로우**를 순서대로 진행하며, 각 단계 산출물을 **개별 마크다운 파일**에 기록한다.
사용자는 파일을 확인하고 피드백하며, 완료 후 하나의 설계 초안 파일로 통합한다.

이 스킬은 **Larman 스타일 OOD**(*Applying UML and Patterns*)에 기반한다:
1. 아키텍처와 계층 분해로 객체가 살 "장소"를 먼저 결정
2. Use Case Realization으로 객체 간 협력을 메시지 교환 단위로 표현
3. GRASP 패턴으로 책임을 클래스에 할당
4. 필요한 곳에만 GoF 디자인 패턴 적용
5. 설계 클래스 다이어그램(DCD)으로 구현 가능한 명세 확정
6. 영속성과 횡단 관심사로 마무리

---

## OOA 의존성 (필수 검증)

이 스킬은 **OOA 산출물 없이 동작하지 않는다.** 시작 전에 다음 중 하나가 반드시 존재해야 한다:

- `docs/usecase/[project-name]-usecase-design.md` (메인 OOA 설계서)
- `docs/usecase/drafts/[feature-name]/[feature-name]-draft.md` (통합 OOA 초안)

존재하지 않으면 **즉시 실행을 중단**하고 사용자에게 다음을 안내한다:

```
OOD를 시작하려면 먼저 OOA(유스케이스 분석)가 완료되어야 합니다.
다음 중 하나가 필요합니다:
- docs/usecase/[project]-usecase-design.md (메인 설계서)
- docs/usecase/drafts/[feature]/[feature]-draft.md (통합 초안)

OOA부터 시작하려면 uc-new-project 스킬을 사용해주세요.
```

OOD 6단계의 모든 입력은 OOA 산출물에서 추출한다. **OOA → OOD 추적성**이 핵심 가치이므로, 추적 불가능한 설계 요소는 ood-review에서 CRITICAL로 분류된다.

---

## 파일 기반 출력 규칙 (핵심)

**이 스킬은 클로드 코드 환경에서 사용한다.** 모든 산출물은 채팅이 아닌 파일에 기록한다.

### 원칙

1. **채팅에는 안내만, 내용은 파일에.** 산출물 본문(표·다이어그램·클래스 정의)을 채팅에 출력하지 않는다.
2. **단계별 개별 파일.** 각 단계의 산출물은 별도 `.md` 파일로 저장한다.
3. **파일로 확인 요청.** 단계 완료 시 "파일을 확인해주세요"로 안내한다.
4. **파일을 직접 편집.** 수정 요청이 오면 해당 파일을 편집한다.
5. **최종 통합.** 6단계 완료 후 단계별 파일을 하나의 초안으로 합친다.

### 채팅 출력 패턴

```
# 단계 완료 시 채팅 메시지 (예시)
1단계 아키텍처·계층 분해를 작성했습니다.
→ docs/design/drafts/[feature]/step1-architecture.md

확인 후 피드백 주세요. 수정할 부분이 있으면 말씀해주시고,
괜찮으면 다음 단계로 진행하겠습니다.
```

**절대 하지 않을 것:** 표·classDiagram·sequenceDiagram·코드 조각을 채팅에 직접 출력하는 것.

---

## 디렉토리 구조

```
[project-root]/
└── docs/
    ├── usecase/                                    ← OOA (입력, 변경 없음)
    │   ├── [project-name]-usecase-design.md
    │   └── drafts/[feature-name]/
    │       └── [feature-name]-draft.md
    │
    └── design/                                     ← OOD (이 스킬이 생성)
        ├── [project-name]-design.md                ← Phase 2 ood-merge가 생성
        ├── drafts/
        │   └── [feature-name]/                     ← 기능별 폴더
        │       ├── step1-architecture.md
        │       ├── step2-interactions.md
        │       ├── step3-responsibilities.md
        │       ├── step4-design-patterns.md
        │       ├── step5-class-diagram.md
        │       ├── step6-cross-cutting.md
        │       └── [feature-name]-design-draft.md  ← 최종 통합본
        └── deprecated/
```

> **Phase 1 안내**: 현재 OOD는 draft 단위로 사용한다. 메인 설계서(`[project]-design.md`) 병합은 Phase 2의 `ood-merge` 스킬 도입 후 지원된다.

---

## 단계별 파일 공통 헤더

모든 단계 파일은 아래 헤더로 시작한다:

```markdown
# Step N: [단계명]

> 프로젝트: [project-name]
> 기능: [feature-name]
> 작성일: [날짜]
> OOA 입력: [참조한 OOA 파일 경로]
> 상태: ✏️ 작성중 | ✅ 확인완료
```

사용자가 확인하면 상태를 `✅ 확인완료`로 변경한다.

---

## 진행 규칙

1. **반드시 순서대로 진행한다.** 단계를 건너뛰지 않는다.
2. **각 단계를 파일로 저장한 뒤 확인을 요청한다.**
3. **사용자가 수정을 요청하면** 해당 파일을 직접 편집하고 다시 확인을 요청한다.
4. **이전 단계의 파일과 OOA 입력 파일을 다음 단계 작성 시 참조한다.**
5. **6단계 완료 후 통합 파일을 생성한다.**
6. **OOA 산출물의 ID·이름을 그대로 인용한다.** UC ID, 엔티티명, 상태명은 OOA에서 정의된 표기를 변경 없이 사용한다.

---

## 시작 절차

1. **OOA 산출물 검증** (위 "OOA 의존성" 섹션 참조).
   ```bash
   ls docs/usecase/
   ls docs/usecase/drafts/
   ```
2. 사용자에게 다음을 확인한다:
   - 어떤 OOA 산출물을 입력으로 사용할지 (메인 설계서 / 특정 feature 초안)
   - OOD 산출물의 **feature 이름** (보통 OOA feature 이름과 동일하게 권장)
3. 디렉토리를 생성한다:
   ```bash
   mkdir -p docs/design/drafts/[feature-name]
   mkdir -p docs/design/deprecated
   ```
4. 6단계 워크플로우를 시작한다.

---

## Mermaid 다이어그램 규칙

모든 단계의 산출물에는 **Mermaid 다이어그램을 필수로 포함**한다.
다이어그램은 표/텍스트 산출물 **아래에** 배치하며, 마크다운 코드 블록(```mermaid)으로 작성한다.

**공통 작성 규칙:**
- 노드 텍스트(레이블)에 한글 사용 가능. 단, 클래스명·인터페이스명·메서드명은 **영문** 사용(언어 무관 UML 표기).
- 복잡한 다이어그램은 하위 그래프(subgraph)로 그룹핑한다.
- 노드 ID는 영문, 표시 레이블은 한글 또는 영문 클래스명. 예: `OrderService["OrderService"]`.
- 다이어그램이 지나치게 커지면 UC 단위 또는 패키지 단위로 분할한다.

**언어 무관 UML 표기:**
- 가시성: `+`(public), `-`(private), `#`(protected), `~`(package)
- 메서드 시그니처: `+ getName(): String`, `+ findById(id: Long): Order`
- 컬렉션: `List~Order~`, `Map~String, Customer~`
- 관계 화살표: `<|--`(상속), `*--`(합성), `o--`(집약), `-->`(연관), `..|>`(인터페이스 구현), `..>`(의존)

---

## 6단계 워크플로우

### 1단계: 아키텍처 스타일 결정 + 계층/패키지 분해

**파일:** `docs/design/drafts/[feature]/step1-architecture.md`

OOA의 **도메인 모델**, **시스템 경계**, **BCE 분석**을 읽고, 객체들이 살 "장소"를 결정한다.
아키텍처 스타일을 선택하고, 계층/패키지를 정의하며, BCE를 계층에 매핑한다.

**파일 내용:**

```markdown
# Step 1: 아키텍처 스타일 + 계층/패키지 분해

> 프로젝트: [project-name]
> 기능: [feature-name]
> 작성일: [날짜]
> OOA 입력: docs/usecase/.../[feature]-draft.md
> 상태: ✏️ 작성중

## BCE 입력 요약

OOA의 BCE 분석에서 도출된 객체들을 카테고리별로 정리한다. 이 스킬의 모든 후속 단계는 이 표에서 출발한다.

| BCE 유형 | 객체 | 원천 UC |
|---------|------|--------|
| Boundary | 주문 입력 화면, 주문 API | UC-01 |
| Control | 주문 처리기 | UC-01, UC-02 |
| Entity | Order, OrderItem, Customer | 도메인 모델 |

## 1. 아키텍처 스타일 결정

| 후보 스타일 | 적합도 | 장점 | 단점 | NFR 연계 |
|------------|------|------|------|---------|
| Layered | ... | ... | ... | ... |
| Hexagonal (Ports & Adapters) | ... | ... | ... | ... |
| Clean Architecture | ... | ... | ... | ... |
| MVC | ... | ... | ... | ... |

**선택:** [선택한 스타일]
**근거:** [선택 이유 — OOA 시스템 경계, 외부 액터 수, 도메인 복잡도 등을 고려]

## 2. 계층/패키지 분해

| 패키지 | 책임 | 허용 의존 (이 패키지가 의존 가능한 곳) | 금지 의존 |
|--------|------|----------------------------------|----------|
| presentation | UI/API 어댑터, 외부 액터와의 입출력 | application | domain, infrastructure |
| application | UC별 조정자(Application Service), 트랜잭션 경계 | domain | presentation, infrastructure |
| domain | 엔티티, 값 객체, 도메인 서비스, 비즈니스 규칙 | (없음) | 모든 외부 |
| infrastructure | DB, 외부 API, 메시지 브로커 등 어댑터 | domain (인터페이스 구현) | presentation, application |

## 3. BCE → 계층 매핑

| BCE | 객체 | 배치 패키지 | 비고 |
|-----|------|-----------|------|
| Boundary | 주문 입력 화면 | presentation | Web UI |
| Boundary | 주문 API | presentation | REST endpoint |
| Control | 주문 처리기 | application | OrderApplicationService 후보 |
| Entity | Order | domain | aggregate root |
| Entity | OrderItem | domain | Order의 합성 부분 |
| Entity | Customer | domain | aggregate root |

## 4. 외부 의존성 (인프라)

OOA 시스템 경계의 "외부 시스템"에 해당하는 항목을 인터페이스(port) 형태로 식별한다.

| 외부 시스템 | 포트 인터페이스 (domain에 정의) | 어댑터 (infrastructure에 구현) |
|------------|----------------------------|--------------------------|
| 결제 시스템 | PaymentGateway | StripePaymentAdapter |
| 알림 시스템 | NotificationSender | EmailNotificationAdapter |

## 5. 계층 의존도 다이어그램

(Mermaid flowchart TB — subgraph로 계층 묶고 화살표로 의존 방향)
```

**주의사항:**
- 의존 방향은 항상 한 방향이어야 한다. 순환 의존이 있으면 계층 분할을 재검토.
- BCE → 계층 매핑은 1:1로 추적 가능해야 한다. 매핑되지 않은 BCE 객체가 있으면 계층을 더 추가하거나 객체를 재정의.
- 외부 시스템은 반드시 domain에 인터페이스(port)를 두고 infrastructure에 어댑터를 두는 의존성 역전 원칙(DIP)을 따른다.

**Mermaid: 계층 의존도** — `flowchart TB`로 작성. 각 계층을 `subgraph`로 그룹핑하고, 화살표는 위→아래(presentation → application → domain ← infrastructure) 방향. 금지된 의존(붉은 점선) 표기는 선택.

**→ 파일 저장 후 확인 요청. 확인되면 상태를 ✅로 변경하고 2단계로 진행.**

---

### 2단계: Use Case Realization (Interaction 정의)

**파일:** `docs/design/drafts/[feature]/step2-interactions.md`

OOA의 **시나리오**, **예외**, **사전/사후조건**, **BCE 상호작용**을 읽고, 각 UC를 객체 간 메시지 교환으로 표현한다.
이 단계의 시퀀스 다이어그램은 OOA 시퀀스보다 **구체적이다** — participant 이름이 구체 클래스/서비스명이고, 메시지는 메서드 호출 단위다.

**파일 내용:**

```markdown
# Step 2: Use Case Realization

> 프로젝트: [project-name]
> 기능: [feature-name]
> 작성일: [날짜]
> OOA 입력: step2-scenarios.md, step7-exceptions.md, step8-conditions.md
> 상태: ✏️ 작성중

## UC-01: [유스케이스명]

### Realization 헤더

| 항목 | 내용 |
|------|------|
| 트리거 | 사용자가 주문 버튼 클릭 |
| 참여 객체 | OrderController, OrderApplicationService, Order, OrderRepository, PaymentGateway |
| 사전조건 (OOA) | 사용자가 로그인되어 있어야 함 |
| 사후조건 (OOA, 성공 시) | 주문 상태가 PENDING으로 생성됨 |
| 결과 | 주문 ID 반환 |

### 객체 협력 표

| 단계 | 송신자 | 메시지 | 수신자 | 반환 |
|------|--------|--------|--------|------|
| 1 | Customer (액터) | placeOrder(items) | OrderController | OrderResponse |
| 2 | OrderController | createOrder(request) | OrderApplicationService | Order |
| 3 | OrderApplicationService | new Order(items, customer) | Order (생성) | Order 인스턴스 |
| 4 | OrderApplicationService | save(order) | OrderRepository | void |
| 5 | OrderApplicationService | charge(order.total) | PaymentGateway | PaymentResult |
| 6 | OrderApplicationService | confirm() | Order | void |

### 시퀀스 다이어그램

(Mermaid sequenceDiagram — participant마다 소속 패키지를 노트로 표기, alt/else로 대안 흐름, break로 예외)

---

## UC-02: [유스케이스명]
(동일 형식 반복)
```

**주의사항:**
- 각 UC마다 Realization 1세트를 만든다. OOA의 모든 UC가 빠짐없이 포함되어야 한다.
- participant 이름은 **구체 클래스/서비스명**(영문). OrderService 같은 모호한 이름이 아니라 OrderApplicationService, OrderRepository, PaymentGateway 등 책임이 명확한 이름.
- 각 participant는 1단계에서 정의한 패키지 중 하나에 속한다. 시퀀스 다이어그램에 `Note over OrderController: presentation` 형태로 명시.
- 대안 흐름(OOA의 alternative flow)은 `alt/else` 블록, 예외 흐름(OOA의 exception)은 `break` 블록으로 표현.
- 메시지는 메서드 호출 단위다. "주문을 처리한다" 같은 추상적 메시지는 금지. `createOrder(request)`처럼 구체적으로.
- 1단계의 의존 방향 규칙을 위반해서는 안 된다 (예: domain이 presentation을 호출하면 안 됨).

**Mermaid: sequenceDiagram** — UC당 1개. participant에 영문 클래스명, alt/else로 대안 흐름, break로 예외. 대규모 UC는 핵심 흐름과 예외를 별도 다이어그램으로 분리 가능.

**→ 파일 저장 후 확인 요청. 확인되면 3단계로 진행.**

---

### 3단계: GRASP 기반 책임 할당

**파일:** `docs/design/drafts/[feature]/step3-responsibilities.md`

OOA의 **도메인 모델**과 **변수 식별**을 읽고, 2단계에서 식별한 객체들에게 책임을 할당한다.
GRASP 패턴(Information Expert, Creator, Controller, Low Coupling, High Cohesion, Polymorphism, Pure Fabrication, Indirection, Protected Variations)을 적용한다.

**파일 내용:**

```markdown
# Step 3: GRASP 기반 책임 할당

> 프로젝트: [project-name]
> 기능: [feature-name]
> 작성일: [날짜]
> OOA 입력: step4-domain-model.md, step3-variables.md
> 상태: ✏️ 작성중

## 1. 책임 카탈로그

2단계의 메시지 교환에서 식별된 책임을 모두 나열한다.

| 책임 ID | 설명 | 유형 | 원천 UC |
|---------|------|------|--------|
| R01 | 주문 합계 금액 계산 | doing | UC-01 |
| R02 | 주문 생성 시간 기록 | knowing | UC-01 |
| R03 | 주문 상태 전이 | doing | UC-01, UC-02 |
| R04 | 결제 게이트웨이 호출 | doing | UC-01 |
| R05 | UC-01 흐름 조정 | doing | UC-01 |

**유형 정의:**
- **knowing**: 데이터/상태를 알고 있어야 하는 책임 (보통 엔티티에 할당)
- **doing**: 행위/계산/조정을 수행하는 책임

## 2. GRASP 할당 표

각 책임을 어떤 클래스에 할당하고 어떤 GRASP 패턴을 적용했는지 기록한다.

| 책임 ID | 할당 클래스 | 적용 패턴 | 근거 |
|---------|-----------|----------|------|
| R01 | Order | Information Expert | 합계 계산에 필요한 OrderItem 정보를 Order가 가짐 |
| R02 | Order | Information Expert | 주문 생성 시간은 Order의 본질 속성 |
| R03 | Order | Information Expert | 상태는 Order 자신의 것 |
| R04 | OrderApplicationService | Pure Fabrication, Low Coupling | 외부 시스템 의존을 entity에서 분리 |
| R05 | OrderApplicationService | Controller (Use Case Controller) | UC-01의 흐름 조정 |

## 3. Controller 목록

| UC ID | Controller 클래스 | 유형 | 비고 |
|-------|-----------------|------|------|
| UC-01 | OrderApplicationService | Use Case Controller | 단일 UC 전담 |
| UC-02 | OrderApplicationService | Use Case Controller | 동일 클래스가 두 UC 처리 |
| UC-03 | RefundApplicationService | Use Case Controller | |

**Bloated Controller 경고:** 한 Controller가 6개 이상의 UC를 담당하면 분리를 검토.

## 4. 책임 할당 클래스 다이어그램 (초안)

(Mermaid classDiagram — **속성 없이 메서드만**. Step5에서 가시성·타입 포함 완전형으로 확장됨)
```

**Step3 vs Step5 경계 (중요):**

| 항목 | Step3 (책임 할당) | Step5 (DCD) |
|------|----------------|------------|
| 다이어그램 목적 | 책임 할당 확인 | 구현 가능 명세 |
| 속성 | **없음** (메서드만) | 가시성/타입 포함 완전 |
| 메서드 | 이름만 | 완전 시그니처+반환 |
| 관계선 | 연관만 (`-->`) | 모든 UML 관계 (상속/합성/집약/구현/의존) |
| 스테레오타입 | 없음 | «entity»/«service»/«repository»/«controller» |
| 추가 산출 | GRASP 근거표 | 의존성·인터페이스·가시성·패키지 배치 |

**Step5는 Step3의 단순 복제가 아니다.** Step5에서는 Step1의 계층 규칙과 Step4의 패턴 적용이 더해진 확장 결과여야 한다.

**주의사항:**
- 책임 카탈로그는 2단계 메시지 교환의 모든 메시지를 cover해야 한다. 누락된 책임이 있으면 2단계로 돌아가 메시지를 보충.
- Information Expert가 가장 먼저 적용된다 — "이 데이터를 가진 객체는 누구인가?"가 첫 질문.
- Pure Fabrication은 도메인 객체에 자연스럽지 않은 책임(외부 호출, 트랜잭션 조정 등)을 분리할 때 사용. 남용 금지.
- Controller는 UC당 하나의 일관된 클래스에 모은다. 여러 클래스에 흩뿌리지 않는다.

**Mermaid: classDiagram (초안)** — 속성 없이 메서드명만. 클래스 간 연관선만 표시.

**→ 파일 저장 후 확인 요청. 확인되면 4단계로 진행.**

---

### 4단계: GoF 디자인 패턴 적용

**파일:** `docs/design/drafts/[feature]/step4-design-patterns.md`

OOA의 **상태 모델**(State 패턴 힌트), **변수 식별의 종속변수 결정 요인**(Strategy 힌트), **도메인 규칙**(Specification 힌트)을 읽고, 필요한 경우에만 GoF 패턴을 적용한다.

**핵심 원칙: 패턴을 위한 패턴 금지.** 모든 패턴 적용은 **OOA에서 도출된 구체적 문제 상황**에서 출발해야 한다.

**파일 내용:**

```markdown
# Step 4: GoF 디자인 패턴 적용

> 프로젝트: [project-name]
> 기능: [feature-name]
> 작성일: [날짜]
> OOA 입력: step5-state-model.md, step3-variables.md, step4-domain-model.md (도메인 규칙)
> 상태: ✏️ 작성중

## 1. 패턴 후보 평가

OOA에서 도출된 문제 상황별로 후보 패턴을 평가한다.

| 문제 상황 | OOA 근거 | 후보 패턴 | 장단점 | 채택 여부 | 근거 |
|----------|---------|----------|------|---------|------|
| Order의 상태에 따라 허용 행위가 달라짐 | step5 상태 모델 | State | 상태별 분기 제거 / 클래스 수 증가 | 채택 | 5개 상태, 각 상태당 3개 이상 메서드 분기 → 충분히 복잡 |
| 결제 수단이 다양 | UC-01 변수 식별 | Strategy | 결제 알고리즘 교체 가능 / 추상화 비용 | 채택 | 신용카드/계좌이체/포인트 3종, 확장 예정 |
| 주문 검증 규칙 다수 | step4 도메인 규칙 | Specification | 규칙 조합 가능 / 클래스 폭발 | 보류 | 규칙 3개로 단순. if문으로 충분 |
| 주문 생성 절차 복잡 | UC-01 시나리오 | Builder | 단계별 생성 / 작은 객체에는 과도 | 보류 | 생성자 파라미터 4개로 충분 |

## 2. 채택 패턴 적용

### 패턴 1: State (Order 상태 관리)

| 항목 | 내용 |
|------|------|
| 분류 | 행위(Behavioral) |
| 참여 클래스 | Order(Context), OrderState(State), CreatedState/PaidState/CancelledState 등(ConcreteState) |
| 매핑 역할 | OOA 상태 모델의 각 상태 = ConcreteState 1개 |

(Mermaid classDiagram — Order, OrderState 추상 클래스, ConcreteState 5개)

### 패턴 2: Strategy (결제 수단)

| 항목 | 내용 |
|------|------|
| 분류 | 행위(Behavioral) |
| 참여 클래스 | PaymentService(Context), PaymentStrategy(Strategy), CreditCardPayment/BankTransferPayment/PointPayment(ConcreteStrategy) |
| 매핑 역할 | OOA 변수 식별의 "결제 수단" 독립변수 = Strategy 선택 입력 |

(Mermaid classDiagram)

## 3. 반증 표 (필수)

채택한 모든 패턴마다 "이 패턴 없이 풀 수 있는가?"에 답한다. 비어있으면 over-engineering 의심.

| 패턴 | 반증: 이 패턴 없이 풀 수 있는가? | 답변 |
|------|------------------------------|------|
| State | if/switch로 상태 분기를 한 메서드에 모을 수 있음 | 가능하지만 5개 상태 × 3개 메서드 = 15개 분기. 상태 추가 시 모든 메서드 수정 필요. State 패턴이 명백히 우위. |
| Strategy | if문으로 결제 수단 분기 가능 | 가능. 그러나 결제 수단이 확장 예정(요구사항 명시)이고, 각 알고리즘이 외부 시스템 호출을 포함해 격리가 필요. Strategy 채택 정당. |
```

**주의사항:**
- 1차 권장 패턴(자주 정당화되는 10개): **Strategy, State, Factory Method, Template Method, Observer, Composite, Decorator, Facade, Repository, Specification**. 외 패턴은 "추가 검토 필요" 플래그.
- 모든 채택 패턴은 반증 표를 반드시 가져야 한다. **반증 없는 패턴 채택은 ood-review에서 CRITICAL.**
- 패턴 적용 자체가 목적이 되어서는 안 된다. "OOA에 이런 문제가 있다 → 이 패턴이 적합하다 → 이 패턴 없이는 풀기 어렵다" 흐름이 명시적이어야 한다.
- Repository 패턴은 6단계에서 자세히 다룬다 (이 단계에서는 언급만).

**Mermaid: 패턴별 classDiagram** — 각 채택 패턴마다 독립 다이어그램. 필요 시 패턴 동작을 sequenceDiagram으로 추가.

**→ 파일 저장 후 확인 요청. 확인되면 5단계로 진행.**

---

### 5단계: 설계 클래스 다이어그램 (DCD)

**파일:** `docs/design/drafts/[feature]/step5-class-diagram.md`

OOA의 **도메인 모델 엔티티 속성**과 **상태 모델 state 필드**를 읽고, 3단계의 책임 할당 + 4단계의 패턴 적용을 종합하여 **구현 가능한 설계 클래스 다이어그램**을 만든다.

이 단계의 다이어그램은 **개발자가 그대로 코드로 옮길 수 있는** 수준이어야 한다.

**파일 내용:**

```markdown
# Step 5: 설계 클래스 다이어그램 (DCD)

> 프로젝트: [project-name]
> 기능: [feature-name]
> 작성일: [날짜]
> OOA 입력: step4-domain-model.md, step5-state-model.md
> 상태: ✏️ 작성중

## 1. 클래스 상세

### Order «entity»

**패키지:** domain
**스테레오타입:** «entity», «aggregate root»
**원천:** OOA 도메인 모델 Order, Step3 R01-R03, Step4 State 패턴 Context

| 가시성 | 이름 | 타입 | 설명 |
|--------|------|------|------|
| - | id | OrderId | 주문 식별자 (값 객체) |
| - | items | List~OrderItem~ | 주문 항목 (합성) |
| - | customer | Customer | 주문한 고객 (연관) |
| - | state | OrderState | 현재 상태 (Step4 State 패턴) |
| - | createdAt | Instant | 생성 시각 |

| 가시성 | 메서드 시그니처 | 반환 | 설명 |
|--------|--------------|------|------|
| + | create(items: List~OrderItem~, customer: Customer) | Order | 정적 팩토리 (Step3 R02 Creator) |
| + | totalAmount() | Money | 합계 계산 (Step3 R01) |
| + | confirm() | void | 확정 전이 (Step3 R03) |
| + | cancel(reason: String) | void | 취소 전이 |
| - | transitionTo(newState: OrderState) | void | 상태 변경 (State 패턴) |

**의존:** OrderItem (합성), Customer (연관), OrderState (집약)

%% traced-from: OOA Order entity, UC-01, UC-02, Step3 R01-R03, Step4 State

---

### OrderApplicationService «service»

**패키지:** application
**스테레오타입:** «service», «use case controller»
**원천:** Step3 R04-R05, BCE Control "주문 처리기"

| 가시성 | 이름 | 타입 | 설명 |
|--------|------|------|------|
| - | orderRepository | OrderRepository | DI |
| - | paymentGateway | PaymentGateway | DI |

| 가시성 | 메서드 시그니처 | 반환 | 설명 |
|--------|--------------|------|------|
| + | createOrder(request: CreateOrderRequest) | OrderResponse | UC-01 |
| + | confirmOrder(orderId: OrderId) | void | UC-02 |

**의존:** Order, OrderRepository, PaymentGateway

%% traced-from: BCE Control, UC-01, UC-02, Step3 R04-R05

---

(다른 클래스들도 동일 형식)

## 2. 인터페이스 목록

| 인터페이스 | 메서드 | 구현 클래스 | 패키지 |
|-----------|--------|-----------|--------|
| OrderRepository | save, findById, findByCustomer | JpaOrderRepository | infrastructure |
| PaymentGateway | charge, refund | StripePaymentAdapter | infrastructure |
| OrderState | confirm, cancel, allowedTransitions | CreatedState, PaidState, ... | domain |

## 3. 통합 클래스 다이어그램

(Mermaid classDiagram — 모든 클래스, 가시성, 타입, 메서드 시그니처, 모든 UML 관계 포함)
```

**주의사항:**
- 모든 클래스는 **스테레오타입**(«entity»/«service»/«repository»/«controller»/«value object»/«aggregate root»)을 가져야 한다.
- 모든 클래스는 **소속 패키지**를 명시해야 한다. 1단계의 패키지 정의와 일치해야 한다.
- 모든 클래스는 **`%% traced-from:` 주석**을 가져야 한다. 추적 가능하지 않은 클래스는 ood-review에서 CRITICAL.
- 메서드 시그니처는 **언어 무관 UML 표기**(`+ method(param: Type): ReturnType`).
- Step5는 Step3의 확장이지 복제가 아니다. **Step3에 없던 정보**(가시성, 타입, 시그니처, 스테레오타입, 패키지, 의존성, Step4 패턴 반영)가 추가되어야 한다.
- 1단계 의존 방향 규칙을 위반하는 의존성이 있으면 즉시 수정.

**Mermaid: classDiagram** — 모든 클래스를 한 다이어그램에 담거나, 패키지/UC 단위로 분할. 관계 화살표는 모든 UML 종류 사용.

**→ 파일 저장 후 확인 요청. 확인되면 6단계로 진행.**

---

### 6단계: 영속성 + 횡단 관심사

**파일:** `docs/design/drafts/[feature]/step6-cross-cutting.md`

OOA의 **사전/사후조건**(트랜잭션 경계), **예외**(에러 정책), **상태 모델 불허 전이**(가드/예외)를 읽고, 인프라 측면의 결정을 마무리한다.

**파일 내용:**

```markdown
# Step 6: 영속성 + 횡단 관심사

> 프로젝트: [project-name]
> 기능: [feature-name]
> 작성일: [날짜]
> OOA 입력: step7-exceptions.md, step8-conditions.md, step5-state-model.md (불허 전이)
> 상태: ✏️ 작성중

## 1. Repository 목록

| Repository 인터페이스 | 대상 Aggregate | 주요 메서드 | 쿼리 의도 |
|--------------------|--------------|----------|---------|
| OrderRepository | Order | save, findById, findByCustomer | 고객별 주문 조회는 UC-04 근거 |
| CustomerRepository | Customer | save, findById, findByEmail | UC-01 사전조건(고객 검증) |

각 Repository 인터페이스는 **domain 패키지**에 정의되고, 구현체는 **infrastructure 패키지**에 둔다(DIP).

## 2. 트랜잭션 경계

| UC ID | 시작 지점 | 커밋 지점 | 격리 수준 | 롤백 조건 |
|-------|---------|---------|---------|---------|
| UC-01 | OrderApplicationService.createOrder 진입 | createOrder 정상 종료 | READ_COMMITTED | 결제 실패, 검증 실패 |
| UC-02 | OrderApplicationService.confirmOrder 진입 | confirmOrder 정상 종료 | READ_COMMITTED | 상태 전이 불허 |

## 3. 에러 정책

OOA의 모든 예외(step7)를 설계상 예외 클래스로 매핑한다.

| OOA 예외 ID | OOA 예외 설명 | 설계 예외 클래스 | 처리 계층 | 응답 형식 |
|-----------|------------|--------------|---------|---------|
| UC-01-EX1 | 입력 데이터 누락 | InvalidOrderRequestException | presentation (handler) | 400 + 필드별 메시지 |
| UC-01-EX2 | 결제 실패 | PaymentFailedException | application | 402 + 결제 코드 |
| UC-02-EX1 | 상태 전이 불허 | IllegalStateTransitionException | application | 409 + 현재 상태 |
| UC-02-EX2 | DB 저장 실패 | RepositoryException | infrastructure → application | 500, 재시도 후 실패 |

**불허 전이 매핑:**

OOA 상태 모델의 모든 불허 전이는 IllegalStateTransitionException으로 일괄 처리한다.

| 출발 상태 | 도착 상태 | 불허 사유 | 던지는 메서드 |
|---------|---------|---------|------------|
| PAID | CREATED | 결제 완료된 주문은 되돌릴 수 없음 | Order.cancel() |
| CANCELLED | CONFIRMED | 취소된 주문은 확인 불가 | Order.confirm() |

## 4. 횡단 관심사

| 관심사 | 적용 지점 | 구현 전략 |
|-------|---------|---------|
| 로깅 | application 계층 진입/종료 | 데코레이터 또는 AOP |
| 보안 | presentation 계층 인증 검증 | 미들웨어/필터 |
| 캐싱 | Customer 조회 | Repository 데코레이터 |
| 감사(audit) | Order 상태 변경 | Domain Event + 이벤트 리스너 |

## 5. 트랜잭션 경계 시퀀스 (선택)

(Mermaid sequenceDiagram — UC-01의 트랜잭션 경계를 rect 배경 구간으로 표시)
```

**주의사항:**
- OOA의 모든 예외(step7)가 빠짐없이 매핑되어야 한다. 누락 시 ood-review CRITICAL.
- OOA 상태 모델의 모든 불허 전이가 가드 메서드 또는 예외로 표현되어야 한다.
- Repository는 항상 인터페이스를 domain에, 구현을 infrastructure에 두어 DIP를 따른다.
- 사전/사후조건은 application 서비스의 메서드 시작/종료 시점에 매핑된다 — 이를 코드 리뷰나 테스트에서 확인 가능하도록 명시.

**Mermaid: 트랜잭션 경계** — sequenceDiagram의 `rect rgb(255, 240, 220)` 등으로 트랜잭션 구간을 시각화.

**→ 파일 저장 후 확인 요청. 확인되면 통합 단계로 진행.**

---

## 최종 통합

6단계 파일이 모두 `✅ 확인완료` 상태가 되면, 하나의 설계 초안 파일로 통합한다.

**통합 방법:**
1. `step1` ~ `step6` 파일을 순서대로 읽는다.
2. 각 파일의 헤더(Step N, 상태 등)를 제거하고 본문만 추출한다.
3. **맨 앞에 OOA → OOD 추적성 매트릭스**를 삽입한다.
4. 초안 문서 구조에 맞게 재구성한다.

**파일:** `docs/design/drafts/[feature]/[feature-name]-design-draft.md`

```markdown
# [기능명] OOD 설계 초안

> 프로젝트: [project-name]
> 작성일: [날짜]
> OOA 입력: [참조한 OOA 파일들]
> 상태: 초안 (draft)

## 0. OOA → OOD 추적성 매트릭스

| OOA 요소 | OOD 매핑 대상 | 1차 위치 |
|---------|------------|--------|
| UC-ID | Use Case Realization, Controller | Step2, Step3 |
| 시나리오 단계 | Sequence 메시지 | Step2 |
| 액터 | Boundary 클래스, 인터페이스 포트 | Step1, Step5 |
| 도메인 엔티티 | Domain 클래스 «entity» | Step5 |
| 엔티티 관계 | classDiagram 관계 기호 | Step5 |
| 일반화/특수화 | 상속/인터페이스 구현 | Step5 |
| 상태 모델 상태/전이 | State 패턴 또는 state 필드+가드 | Step4, Step5 |
| 불허 전이 | 예외 던지기 + 가드 메서드 | Step6 |
| 독립변수 | 입력 파라미터, Request DTO | Step2, Step5 |
| 상수 | Policy/Configuration 객체 | Step4, Step5 |
| 종속변수 | 반환 타입, Response DTO | Step5, Step6 |
| BCE Boundary | presentation 계층 클래스 | Step1, Step5 |
| BCE Control | application 계층 service | Step1, Step3, Step5 |
| BCE Entity | domain 계층 aggregate | Step5 |
| 사전조건 | 가드 메서드, 인바리언트 검증 | Step6 |
| 사후조건 | 메서드 반환/상태 보장 | Step6 |
| 예외 | 예외 클래스 계층, 처리 정책 | Step6 |

## 1. 아키텍처 + 계층 분해
(step1 내용)

## 2. Use Case Realization
(step2 내용)

## 3. GRASP 책임 할당
(step3 내용)

## 4. 디자인 패턴 적용
(step4 내용)

## 5. 설계 클래스 다이어그램
(step5 내용)

## 6. 영속성 + 횡단 관심사
(step6 내용)
```

통합 완료 후 사용자에게 파일 경로를 안내하고 다음 단계를 제안한다:
- `ood-review`로 OOD 초안 리뷰

> **Phase 1 안내**: 현재 OOD 메인 설계서 병합(`ood-merge`)은 미지원. draft 단위로 사용하고, 메인 통합은 Phase 2 도입을 기다리거나 수동으로 진행한다.
