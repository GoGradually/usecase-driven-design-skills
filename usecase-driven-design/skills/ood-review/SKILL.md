---
name: ood-review
description: OOD 설계 초안 또는 메인 설계서를 6관점에서 리뷰한다. 완전성, OOA 정합성(추적성), SOLID 준수, GRASP 적용 적절성, 결합도·응집도·의존성 방향, 디자인 패턴 적용 타당성을 체계적으로 검토하고 개선점을 제안한다. 리뷰 결과는 마크다운 파일에 기록한다. 'OOD 리뷰', '설계 검토', '클래스 다이어그램 점검', '아키텍처 리뷰' 등의 요청에 사용한다. 리뷰 결과에 따라 수정을 바로 반영하거나 리뷰 리포트만 제공할 수 있다.
---

# OOD 문서 리뷰

## 개요

OOD 초안(draft) 또는 메인 설계서를 체계적으로 리뷰한다.
**6개 관점**에서 검토하고, 발견된 이슈를 등급별로 분류하여 **리뷰 리포트 파일**에 기록한다.

이 스킬은 uc-review와 짝을 이룬다. uc-review가 OOA 산출물의 품질을 보장한다면, ood-review는 OOD 산출물이 OOA를 정확히 이어받았는지, 그리고 객체지향 설계 원칙(SOLID/GRASP/결합도·응집도)을 잘 준수했는지 검증한다.

---

## 파일 기반 출력 규칙 (핵심)

**이 스킬은 클로드 코드 환경에서 사용한다.** 리뷰 결과는 채팅이 아닌 파일에 기록한다.

### 원칙

1. **리뷰 결과를 파일에 기록한다.** 리뷰 리포트를 `.md` 파일로 저장한다.
2. **채팅에는 요약만.** "리뷰를 완료했습니다. CRITICAL 2건, WARNING 4건입니다." 정도만 안내한다.
3. **수정도 파일에서.** 수정 반영 시 원본 OOD 파일을 직접 편집하고 리포트를 갱신한다.

### 채팅 출력 패턴

```
# 리뷰 완료 시 (예시)
OOD 리뷰를 완료했습니다.
→ docs/design/drafts/[feature]/review-report.md

요약: ❌ CRITICAL 2건 | ⚠️ WARNING 4건 | ℹ️ INFO 3건
주요 이슈: OOA 추적 누락 1건, Bloated Controller 1건
자세한 내용은 리포트를 확인해주세요.
수정을 바로 반영할까요?
```

---

## 시작 절차

### 1. 리뷰 대상 확인

```bash
ls docs/design/
ls docs/design/drafts/
```

리뷰 대상이 될 수 있는 파일:
- `docs/design/drafts/[feature]/[feature]-design-draft.md` — 통합 초안
- `docs/design/drafts/[feature]/step*.md` — 개별 단계 파일
- `docs/design/[project-name]-design.md` — 메인 통합 문서 (Phase 2 도입 후)

### 2. OOA 입력 동시 확인

OOD 리뷰는 OOA 정합성(관점 2)을 핵심으로 하므로, 대응하는 OOA 산출물을 함께 읽어야 한다:
- `docs/usecase/[project-name]-usecase-design.md` 또는
- `docs/usecase/drafts/[feature]/[feature]-draft.md`

OOA 산출물이 없으면 리뷰는 가능하지만 관점 2(OOA 정합성)는 N/A로 처리하고 사용자에게 경고한다.

### 3. 리뷰 범위 결정

사용자에게 리뷰 범위를 질문한다:
- **전체 리뷰**: 6개 관점 모두 검토 (기본값)
- **부분 리뷰**: 특정 관점만 검토 (예: "SOLID만 봐줘")
- **단일 step 리뷰**: 특정 step 파일만 (예: "step5만 봐줘")

---

## 리뷰 관점 (6개)

### 관점 1: 완전성 (Completeness)

| 항목 | 검토 내용 |
|------|----------|
| 6단계 존재 여부 | step1~step6 파일이 모두 있는가? add-feature인 경우 step0도 포함 |
| 단계별 필수 표 | 각 step의 필수 표가 모두 작성되었는가? (Step1: 아키텍처 결정/계층/BCE 매핑, Step2: Realization 헤더/메시지 표, Step3: 책임 카탈로그/GRASP 할당/Controller 목록, Step4: 패턴 후보/채택/반증, Step5: 클래스 상세/인터페이스/통합 다이어그램, Step6: Repository/트랜잭션 경계/에러 정책/횡단 관심사) |
| Mermaid 다이어그램 | Step1: 계층 의존도, Step2: 시퀀스(UC당 1개), Step3: classDiagram 초안, Step4: 패턴별 classDiagram, Step5: 통합 classDiagram, Step6: (선택) 트랜잭션 경계 시퀀스 모두 존재하는가? |
| UC 커버리지 | 모든 OOA UC가 Step2에서 Use Case Realization을 가지는가? |
| 엔티티 커버리지 | 모든 OOA 도메인 엔티티가 Step5의 통합 클래스 다이어그램에 «entity»로 반영되었는가? |
| 추적성 매트릭스 | 통합 draft 상단에 OOA → OOD 추적성 매트릭스가 있는가? 17개 행이 모두 채워졌는가? |
| **Step5 ≠ Step3 복제** | Step5가 Step3의 단순 복제가 아닌가? Step5에는 Step3에 없던 가시성·타입·시그니처·스테레오타입·패키지·완전한 UML 관계가 있어야 함 |
| 메타 정보 | 프로젝트명, feature명, 작성일, OOA 입력 경로가 모든 step 파일 헤더에 기재되었는가? |

### 관점 2: OOA 정합성 (Traceability)

**가장 중요한 관점.** OOD가 OOA를 정확히 이어받았는지, 그리고 모든 설계 요소가 OOA 근거를 가지는지 검증한다.

| 항목 | 검토 내용 |
|------|----------|
| **고아 클래스** | Step5의 모든 클래스가 `%% traced-from:` 주석을 가지는가? OOA 근거 없이 등장한 클래스가 있는가? |
| **누락 UC** | OOA의 모든 UC가 Step2의 Use Case Realization에 등장하는가? |
| **누락 엔티티** | OOA 도메인 모델의 모든 엔티티가 Step5에 «entity»로 매핑되었는가? |
| **BCE → 계층 매핑** | OOA BCE 분석의 모든 항목이 Step1 "BCE → 계층 매핑"에 1:1로 매핑되었는가? Boundary→presentation, Control→application, Entity→domain 원칙이 지켜졌는가? |
| **상태 모델 반영** | OOA 상태 모델의 모든 상태가 Step4의 State 패턴 또는 Step5의 state 필드+가드 메서드로 반영되었는가? |
| **불허 전이 → 예외** | OOA 상태 모델의 모든 불허 전이가 Step6의 에러 정책에 예외 클래스로 매핑되었는가? |
| **사전조건 반영** | OOA의 사전조건이 Step6의 가드 메서드 또는 인바리언트 검증으로 반영되었는가? |
| **사후조건 반영** | OOA의 사후조건이 Step5/Step6의 메서드 반환·상태 보장으로 반영되었는가? |
| **예외 매핑** | OOA의 모든 예외(step7)가 Step6의 에러 정책 표에 빠짐없이 매핑되었는가? |
| **변수 식별 반영** | OOA의 독립변수가 Step5의 입력 파라미터/Request DTO로, 종속변수가 반환 타입/Response DTO로 반영되었는가? |
| **일반화/특수화 반영** | OOA의 IS-A 관계가 Step5의 상속(`<\|--`) 또는 인터페이스 구현(`..\|>`)으로 반영되었는가? |
| **관계 유형 반영** | OOA의 연관/집약/합성이 Step5에서 각각 `-->`/`o--`/`*--`로 정확히 매핑되었는가? |
| **추적성 주석 형식** | `%% traced-from: UC-xx, Entity-yy, Step3-Rxx, Step4-패턴` 형식이 일관되게 사용되었는가? |

### 관점 3: SOLID 준수

| 원칙 | 검토 내용 |
|------|----------|
| **SRP** (Single Responsibility) | 각 클래스가 하나의 변경 이유만 가지는가? Step3의 책임 카탈로그를 보면 한 클래스에 7개 이상의 책임이 몰려있지 않은가? |
| **OCP** (Open/Closed) | 확장이 자주 일어날 지점에 Step4의 디자인 패턴이 적용되었는가? (예: 결제 수단이 늘어날 예정인데 if/switch로 분기) |
| **LSP** (Liskov Substitution) | 상속 계층에서 하위 타입이 상위 타입의 계약을 위반하지 않는가? OOA의 일반화/특수화에서 "배타적/완전" 분류가 코드 계약과 충돌하지 않는가? |
| **ISP** (Interface Segregation) | 인터페이스가 사용자별로 분리되었는가? 한 인터페이스에 메서드 10개 이상이 몰려있지 않은가? |
| **DIP** (Dependency Inversion) | Step1의 의존 방향 규칙이 Step5에서 위반되지 않았는가? domain이 infrastructure를 직접 의존하지 않는가? Repository/Gateway가 domain에 인터페이스로 정의되었는가? |

### 관점 4: GRASP 적용 적절성

| 항목 | 검토 내용 |
|------|----------|
| **Information Expert** | knowing 책임이 데이터 소유 클래스에 배정되었는가? (예: 합계 계산이 OrderItem 정보를 가진 Order에 배정) |
| **Creator** | 객체 생성 책임이 합리적인 클래스에 배정되었는가? (Creator의 5가지 조건 중 최소 1개 충족) |
| **Controller** | UC당 Controller가 명시적으로 식별되었는가? Use Case Controller / Facade Controller 구분이 적절한가? |
| **Bloated Controller** | 한 Controller가 6개 이상의 UC를 담당하지 않는가? 한 Controller에 책임이 15개 이상 몰려있지 않은가? |
| **Low Coupling** | 클래스 간 의존성이 최소화되었는가? Step5의 의존 화살표가 한 클래스에서 5개 이상 나가지 않는가? |
| **High Cohesion** | 클래스 내 책임이 응집되어 있는가? 한 클래스 안에 서로 무관한 책임이 섞여있지 않은가? |
| **Pure Fabrication** | 도메인 객체에 자연스럽지 않은 책임(외부 호출/트랜잭션)이 Service로 분리되었는가? 그러나 남용되어 anemic domain이 되지 않았는가? |
| **Polymorphism** | 타입에 따른 분기(if/switch)가 폴리모피즘으로 대체되었는가? Step4의 State/Strategy 적용과 일치하는가? |
| **Indirection** | 결합도를 낮추기 위한 중간 계층이 적절히 사용되었는가? |
| **Protected Variations** | 변동성이 큰 지점이 인터페이스로 보호되었는가? (예: 외부 시스템 변경 가능성 → port/adapter) |

### 관점 5: 결합도 · 응집도 · 의존성 방향

| 항목 | 검토 내용 |
|------|----------|
| **계층 의존 방향 위반** | Step1의 의존 방향 규칙(presentation → application → domain ← infrastructure)을 Step5의 다이어그램이 정확히 따르는가? domain → presentation 같은 역방향 의존이 있는가? |
| **순환 의존** | 클래스 간 또는 패키지 간 순환 의존이 있는가? (A → B, B → A) |
| **패키지 팬아웃** | 한 패키지가 너무 많은 다른 패키지에 의존하지 않는가? |
| **anemic domain** | 도메인 클래스가 데이터만 가지고 행위를 application/service에 모두 위임하는 anemic domain anti-pattern이 발생하지 않았는가? |
| **God Class** | 한 클래스에 메서드 20개 이상, 속성 15개 이상이 몰려있지 않은가? |
| **추상화 수준 혼재** | 한 클래스 또는 한 메서드 안에 비즈니스 로직과 인프라 호출이 섞여있지 않은가? |
| **Pure Fabrication 남용** | Service 클래스가 과도하게 많아 도메인이 비어있지 않은가? |

### 관점 6: 디자인 패턴 적용 타당성

| 항목 | 검토 내용 |
|------|----------|
| **반증 표 존재** | Step4의 모든 채택 패턴이 "이 패턴 없이 풀 수 있는가?" 반증 표를 가지는가? **반증 없는 패턴 채택은 CRITICAL.** |
| **패턴 역할 매핑 정확성** | 각 패턴의 참여 클래스가 GoF 정의의 역할을 정확히 수행하는가? (예: State 패턴에서 Context가 ConcreteState를 직접 알지 않고 State 인터페이스만 의존) |
| **OOA 근거 존재** | 각 패턴이 OOA의 어떤 문제 상황에서 유래했는지 명시되었는가? "패턴을 위한 패턴"이 아닌가? |
| **Over-engineering 경고** | 패턴 적용으로 인해 클래스 수가 비합리적으로 증가하지 않았는가? (예: 상태 2개에 State 패턴, 알고리즘 1개에 Strategy) |
| **권장 패턴 외 채택** | 1차 권장 10개 패턴(Strategy, State, Factory Method, Template Method, Observer, Composite, Decorator, Facade, Repository, Specification) 외 패턴이 채택된 경우, 추가 정당화가 충분한가? |
| **패턴 충돌** | 동일 문제에 두 패턴이 중복 적용되거나 서로 충돌하지 않는가? |

---

## 리뷰 리포트 파일

**파일 위치:**
- 초안 리뷰 시: `docs/design/drafts/[feature]/review-report.md`
- 메인 문서 리뷰 시: `docs/design/review-report-[날짜].md`

**리포트 형식:**

```markdown
# OOD 리뷰 결과

> 대상: [파일명]
> 리뷰일: [날짜]
> 범위: 전체 리뷰 / 부분 리뷰 ([관점])
> 참조 OOA: [경로]

## 요약

| 관점 | 상태 | 이슈 수 |
|------|------|--------|
| 1. 완전성 | ✅/⚠️/❌ | N개 |
| 2. OOA 정합성 (추적성) | ✅/⚠️/❌ | N개 |
| 3. SOLID 준수 | ✅/⚠️/❌ | N개 |
| 4. GRASP 적용 적절성 | ✅/⚠️/❌ | N개 |
| 5. 결합도·응집도·의존성 방향 | ✅/⚠️/❌ | N개 |
| 6. 디자인 패턴 적용 타당성 | ✅/⚠️/❌ | N개 |

## 이슈 목록

### [CRITICAL] 반드시 수정 필요

1. **[OOA 정합성]** Step5의 RefundCalculator 클래스가 `%% traced-from:` 주석이 없고, OOA 어디에도 근거가 없음 (고아 클래스)
   - 위치: step5-class-diagram.md, RefundCalculator
   - 제안: OOA 근거를 추가하거나 클래스를 제거. OOA에 빠진 책임이 있다면 uc-review로 OOA부터 보강.

2. **[디자인 패턴]** Step4에서 Visitor 패턴 채택했으나 반증 표가 비어있음
   - 위치: step4-design-patterns.md, Visitor 섹션
   - 제안: "이 패턴 없이 풀 수 있는가?"에 답변 추가. 답변이 "가능"이고 정당화가 약하면 패턴 제거.

### [WARNING] 수정 권장

1. **[GRASP]** OrderApplicationService가 7개 UC를 담당 (Bloated Controller 경고)
   - 위치: step3-responsibilities.md, Controller 목록
   - 제안: UC-04~UC-07을 OrderQueryService로 분리.

2. **[SOLID]** PaymentService가 결제 수단 분기에 if/elseif 사용 (OCP 위반)
   - 위치: step5-class-diagram.md, PaymentService.charge
   - 제안: Step4의 Strategy 패턴 적용으로 변경.

### [INFO] 참고/개선 가능

1. **[완전성]** Step6의 트랜잭션 경계 시퀀스 다이어그램이 선택 사항이지만 누락됨
   - 위치: step6-cross-cutting.md
   - 제안: 가독성 향상을 위해 추가 권장.
```

상태 기준: ✅ 이슈 없음 | ⚠️ WARNING만 | ❌ CRITICAL 있음

---

## 리뷰 후 행동

리포트 파일을 저장한 뒤, 사용자에게 다음 선택지를 채팅으로 안내한다:

1. **즉시 수정**: CRITICAL/WARNING 이슈를 원본 OOD 파일에 반영하고, 리포트의 해당 항목에 `[수정 완료]` 표시를 추가한다.
2. **리뷰만 확인**: 리포트만 참고하고, 사용자가 나중에 수정한다.
3. **부분 수정**: 특정 이슈만 선택하여 수정한다.

수정 반영 시 원본 파일(step*.md 또는 design-draft.md)을 직접 편집하고, 리포트 파일에 수정 이력을 기록한다:

```markdown
## 수정 이력

| 이슈 | 수정 내용 | 수정일 |
|------|----------|--------|
| CRITICAL-1 | step5에서 RefundCalculator 제거, RefundPolicy로 책임 이전 | [날짜] |
| WARNING-1 | OrderApplicationService → OrderApplicationService + OrderQueryService로 분리 | [날짜] |
```

---

## OOA 보강이 필요한 경우

OOD 리뷰 중 OOA 자체에 결함이 발견되면 (예: 누락된 UC, 모순된 도메인 규칙), 채팅에 다음을 안내한다:

```
OOD 리뷰 중 OOA 보강이 필요한 항목이 발견되었습니다:
- OOA의 도메인 모델에 [엔티티명] 누락
- OOA의 [UC-xx] 시나리오에 [상황] 처리가 빠짐

uc-review로 OOA부터 보강한 후 OOD를 다시 검토하시는 것을 권장합니다.
```

OOD에 패치를 가하기보다 OOA부터 고치는 것이 우선이다 — OOA-OOD 정합성이 핵심 가치이기 때문이다.
