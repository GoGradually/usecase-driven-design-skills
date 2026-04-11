# UseCase & Object-Oriented Design 스킬 사용 가이드

> 버전: v4 (OOD 워크플로우 추가 — Phase 1: ood-new-project / ood-add-feature / ood-review)
> 대상 환경: Claude Code
> 스킬 수: 9개 (OOA 6 + OOD 3)

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
    - [ood-new-project](#57-ood-new-project)
    - [ood-add-feature](#58-ood-add-feature)
    - [ood-review](#59-ood-review)
6. [산출물 디렉토리 구조](#6-산출물-디렉토리-구조)
7. [실전 시나리오별 가이드](#7-실전-시나리오별-가이드)
8. [파일 상태 관리](#8-파일-상태-관리)
9. [FAQ](#9-faq)

---

## 1. 개요

이 스킬 셋은 **유스케이스 주도 분석·설계(Use-Case Driven Analysis & Design)** 를 체계적으로 수행하기 위한 Claude Code 전용 도구입니다. **OOA**(객체지향 분석)부터 **OOD**(객체지향 설계)까지 한 흐름으로 이어집니다.

### 핵심 특징

**파일 기반 출력** — 모든 산출물은 채팅이 아닌 마크다운 파일에 기록됩니다. 채팅에는 파일 경로와 간략한 안내만 표시되며, 실제 내용은 파일을 열어서 확인합니다. 이를 통해 다음과 같은 이점을 얻습니다:

- 긴 채팅 히스토리를 스크롤하며 내용을 찾을 필요가 없음
- 단계별 파일로 분리되어 특정 단계만 빠르게 찾아볼 수 있음
- Git 등 버전 관리 시스템과 자연스럽게 연동
- 수정 시 파일을 직접 편집하므로 변경 이력이 명확

**OOA 완전 커버리지** — 객체지향 분석(OOA)의 세 축을 모두 다룹니다:
- **기능 모델링**: 유스케이스, 시나리오, 시스템 경계
- **구조 모델링**: 도메인 모델, 변수 식별
- **행위 모델링**: 상태 모델 (엔티티 생애주기)

**OOD 6단계 (Larman 스타일)** — OOA를 입력으로 받아 구현 가능한 클래스 설계까지 이어집니다:
- **아키텍처 + 계층 분해**: BCE → 패키지 매핑, 의존 방향 규칙
- **Use Case Realization**: 객체 간 메시지 교환 시퀀스
- **GRASP 책임 할당**: Information Expert, Creator, Controller 등 9개 패턴
- **GoF 디자인 패턴**: 반증 의무 기반 적용
- **설계 클래스 다이어그램(DCD)**: 가시성·타입·시그니처·스테레오타입 포함
- **영속성 + 횡단 관심사**: Repository, 트랜잭션 경계, 에러 정책

**OOA → OOD 연속성 (추적성)** — OOD의 모든 설계 요소(클래스·메서드·예외 등)는 OOA 산출물(UC·엔티티·상태·예외 등)에 추적 가능합니다. OOD 통합 초안의 상단에는 17개 행짜리 추적성 매트릭스가 자동 삽입되며, Step5 클래스마다 `%% traced-from:` 주석이 부여됩니다. ood-review가 추적 누락을 CRITICAL로 검사합니다.

### 스킬 간 관계

```
[OOA 단계]
새 프로젝트 시작          기존 프로젝트에 기능 추가
       │                         │
 uc-new-project            uc-add-feature
       │                         │
       └──────────┬──────────────┘
                  │
              uc-review ← OOA 리뷰 (선택)
                  │
              uc-merge ← OOA 메인 문서로 통합
                  │
             uc-deprecate ← UC 폐기/제거 (필요 시)
                  │
                  ▼
[OOD 단계]
새 OOD 시작              기존 OOD에 기능 추가
       │                         │
 ood-new-project           ood-add-feature
       │                         │
       └──────────┬──────────────┘
                  │
              ood-review ← OOD 리뷰 (선택)
                  │
              (Phase 2: ood-merge / ood-deprecate)
```

`usecase-driven-design`은 OOA 워크플로우의 경량 버전(7단계)으로, 초안/메인 문서 분리 없이 바로 설계서를 만들 때 사용합니다. OOD에는 아직 경량판이 없습니다 (Phase 2 도입 예정).

---

## 2. 설치

### 방법 1: 플러그인으로 설치 (권장)

Claude Code에서 Git 저장소를 마켓플레이스로 등록한 뒤 플러그인을 설치합니다.

```bash
# 1. 마켓플레이스 등록
/plugin marketplace add GoGradually/usecase-driven-design-skills

# 2. 플러그인 설치
/plugin install usecase-driven-design@GoGradually-usecase-driven-design-skills
```

설치 후 스킬은 `usecase-driven-design:uc-new-project` 형태로 네임스페이스가 붙습니다.

### 방법 2: 로컬 개발/테스트

저장소를 클론한 뒤 플러그인 디렉토리로 직접 지정합니다.

```bash
git clone https://github.com/GoGradually/usecase-driven-design-skills.git
claude --plugin-dir ./usecase-driven-design-skills/usecase-driven-design
```

### 방법 3: 수동 설치

스킬 폴더를 직접 복사합니다.

```bash
SKILL_DIR="$HOME/.claude/skills"

for skill in uc-new-project uc-add-feature uc-review uc-merge uc-deprecate usecase-driven-design; do
  cp -r usecase-driven-design/skills/$skill "$SKILL_DIR/"
done
```

---

## 3. 스킬 구성 한눈에 보기

### OOA (분석)

| 스킬 | 용도 | 트리거 키워드 | 단계 | 주요 산출물 |
|------|------|-------------|------|-----------|
| `uc-new-project` | 새 프로젝트 UC 설계 | "새 프로젝트", "프로젝트 시작" | 8단계 | `step1~8.md` → 통합 초안 |
| `uc-add-feature` | 기존 프로젝트에 기능 추가 | "기능 추가", "새 기능 UseCase" | 8단계 + step0 | `step0~8.md` → 통합 초안 |
| `uc-review` | UC 문서 리뷰 | "리뷰", "검토", "초안 확인" | 6개 관점 | `review-report.md` |
| `uc-merge` | 초안을 메인 문서에 병합 | "병합", "머지", "merge" | 2개 시나리오 | 메인 설계서 + 병합 리포트 |
| `uc-deprecate` | UC 폐기/제거 | "폐기", "deprecate", "제거" | 7개 분석 + 실행 | 영향 분석 + 결과 리포트 |
| `usecase-driven-design` | 경량 UC 설계 | `/usecase-driven-design` | 7단계 | `step1~7.md` → 통합 설계서 |

### OOD (설계, Phase 1)

| 스킬 | 용도 | 트리거 키워드 | 단계 | 주요 산출물 |
|------|------|-------------|------|-----------|
| `ood-new-project` | OOA 위에 새 OOD 초안 | "OOD 시작", "설계 초안", "클래스 설계" | 6단계 | `step1~6.md` → 통합 설계 초안 |
| `ood-add-feature` | 기존 OOD에 기능 추가 | "OOD 기능 추가", "설계에 추가" | 6단계 + step0 | `step0~6.md` → 통합 설계 초안 |
| `ood-review` | OOD 문서 리뷰 | "OOD 리뷰", "설계 검토" | 6개 관점 | `review-report.md` |

> **Phase 1 안내**: OOD는 현재 draft 단위로 사용합니다. 메인 설계서 병합(`ood-merge`), 폐기(`ood-deprecate`), 경량판은 Phase 2에서 도입 예정입니다.

---

## 4. 워크플로우 흐름도

### 일반적인 프로젝트 흐름

```
[OOA 단계 — 분석]

1. 프로젝트 시작
   └─→ uc-new-project (8단계 → 초안 생성)

2. 초안 리뷰 (권장)
   └─→ uc-review (리뷰 리포트 → 수정 반영)

3. 메인 문서 생성
   └─→ uc-merge (초안 → 메인 설계서)

4. 기능 추가 (반복)
   └─→ uc-add-feature (8단계 → 새 초안)
       └─→ uc-review (리뷰)
           └─→ uc-merge (메인에 병합)

5. 기능 폐기 (필요 시)
   └─→ uc-deprecate (영향 분석 → 실행)

[OOD 단계 — 설계, OOA 산출물 입력]

6. OOD 시작 (OOA 완료 후)
   └─→ ood-new-project (6단계 → OOD 초안 생성)

7. OOD 리뷰 (권장)
   └─→ ood-review (6관점 — 완전성/OOA 정합성/SOLID/GRASP/결합도/패턴)

8. OOD에 기능 추가 (반복)
   └─→ ood-add-feature (step0 분석 + 6단계 → 새 초안)
       └─→ ood-review (리뷰)
```

### 간단한 설계

규모가 작거나 빠르게 진행할 때는 `usecase-driven-design`만 사용합니다 (OOA 한정):

```
usecase-driven-design (7단계 → 바로 설계서)
```

OOD 경량판은 Phase 2에서 도입 예정입니다.

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
  ... (3~8단계 반복) ...
    ↓
Claude: 8단계 완료 → [feature]-draft.md 통합본 생성
```

#### 생성되는 파일

```
docs/usecase/drafts/[feature-name]/
├── step1-usecases.md        ← 유스케이스 목록
├── step2-scenarios.md        ← 시나리오 + 시퀀스 다이어그램
├── step3-variables.md        ← 독립변수/상수/종속변수 + 관계도
├── step4-domain-model.md     ← 엔티티, 관계, 규칙 + 클래스 다이어그램
├── step5-state-model.md      ← 상태 모델 + 상태 다이어그램
├── step6-system-boundary.md  ← 시스템 경계 + UC 다이어그램
├── step7-exceptions.md       ← 예외 정리
├── step8-conditions.md       ← 사전/사후조건
└── [feature-name]-draft.md   ← 최종 통합본
```

#### 단계별 확인 포인트

| 단계 | 확인할 내용 |
|------|-----------|
| 1단계 | UC 식별이 빠짐없는지, 크기가 적절한지 |
| 2단계 | 기본 흐름이 자연스러운지, 대안 흐름이 충분한지 |
| 3단계 | 변수 분류가 타당한지, 종속변수의 결정 요인이 맞는지 |
| 4단계 | 엔티티가 누락 없는지, 관계가 맞는지 |
| 5단계 | 라이프사이클 엔티티를 빠짐없이 다루는지, 전이가 시나리오와 일치하는지 |
| 6단계 | 내/외부 분리가 올바른지, UC 다이어그램이 경계를 정확히 표현하는지 |
| 7단계 | 예외가 빠짐없는지, 대응이 구체적인지 |
| 8단계 | 조건이 검증 가능한 형태인지, 상태 모델의 출발/도착 상태가 반영되었는지 |

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
Claude: 1~8단계 진행 (uc-new-project와 동일, ID는 기존 이어서)
    ↓
Claude: 통합본 생성
```

#### uc-new-project와의 차이점

| 항목 | uc-new-project | uc-add-feature |
|------|---------------|----------------|
| step0 | 없음 | 기존 문서 분석 파일 생성 (상태 모델 포함) |
| UC ID | UC-01부터 시작 | 기존 마지막 ID 다음부터 |
| 도메인 모델 | 새로 설계 | 기존 모델 확장 (기존/신규 구분) |
| 상태 모델 | 새로 설계 | 기존 상태 모델 확장 (기존 상태 유지 + 신규 추가) |
| 액터 | 새로 정의 | 기존 재사용 + 필요 시 추가 |
| 다이어그램 | 독립적 | 기존 노드를 포함하여 맥락 표현 |

---

### 5.3 uc-review

UseCase 문서를 5개 관점에서 체계적으로 리뷰합니다.

#### 호출 예시

```
"환불 기능 초안을 리뷰해줘."
"메인 설계서를 전체 검토해줘."
"상태 모델만 집중적으로 봐줘."
```

#### 리뷰 5개 관점

| 관점 | 검토 초점 |
|------|----------|
| **완전성** | 8단계 모두 있는지, 빠진 UC/다이어그램 없는지 |
| **일관성** | ID 연속성, 용어 통일, 다이어그램↔표 일치, 상태↔시나리오↔사후조건 정합 |
| **품질** | 시나리오 구체성, 변수 분류 타당성, 상태 모델 완전성, 예외 대응 |
| **구조적 적절성** | UC 크기, 의존성 방향, 관계 정합성, 상태 모델이 개념 수준인지 |
| **기존 문서 정합성** | ID 충돌, 엔티티 충돌, 규칙 모순, 상태 모델 충돌 (기존 문서 있을 때만) |

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
- 상태 모델 통합 (상태 합산, 전이 중복 제거, UC 참조 갱신)
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

#### 영향 분석 7개 관점

| 분석 | 확인 내용 |
|------|----------|
| UC 의존성 | 다른 UC가 이 UC를 참조하는 곳 |
| 변수 연쇄 | 종속변수가 다른 UC의 입력이 되는 경우 |
| 도메인 모델 | 이 UC 전용 엔티티 vs 공유 엔티티 |
| 상태 모델 | 이 UC가 트리거하는 전이, 도달 불가 상태 발생 여부 |
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
| 단계 수 | 7단계 | 8단계 (변수 식별 포함) |
| 변수 식별 | 없음 | 3단계에서 수행 |
| Mermaid | 없음 | 모든 단계에 포함 |
| 상태 모델 | 테이블만 (Mermaid 없음) | 테이블 + stateDiagram |
| 산출물 | 바로 설계서 | 초안 → merge로 설계서 |
| 디렉토리 | `docs/usecase/step*.md` | `docs/usecase/drafts/[feature]/step*.md` |
| 적합한 상황 | 소규모, 빠른 진행 | 중대규모, 체계적 관리 |

---

### 5.7 ood-new-project

OOA가 완료된 프로젝트의 객체지향 설계(OOD) 초안을 처음부터 만듭니다. **6단계 OOD 워크플로우**(아키텍처 → Use Case Realization → GRASP 책임 할당 → 디자인 패턴 → 설계 클래스 다이어그램 → 영속성·횡단 관심사)를 진행합니다.

#### 호출 예시

```
"OOA 끝났으니 이제 OOD 설계를 시작하자."
"order 기능의 클래스 설계를 만들어줘."
"아키텍처 + 클래스 다이어그램을 잡아줘."
```

#### 전제 조건

OOA 산출물이 반드시 존재해야 합니다:
- `docs/usecase/[project-name]-usecase-design.md` (메인 OOA 설계서) 또는
- `docs/usecase/drafts/[feature]/[feature]-draft.md` (통합 OOA 초안)

없으면 `uc-new-project`로 OOA부터 진행합니다.

#### 진행 흐름

```
사용자: OOD 시작 요청 + feature 이름
    ↓
Claude: OOA 산출물 검증 + 디렉토리 생성 → step1 작성 → step1-architecture.md 저장
    ↓
사용자: 파일 확인 → "OK" 또는 "수정해줘"
    ↓
Claude: (수정 시 파일 편집) → step2 작성 → step2-interactions.md 저장
    ↓
  ... (3~6단계 반복) ...
    ↓
Claude: 6단계 완료 → [feature]-design-draft.md 통합본 생성
        (OOA → OOD 추적성 매트릭스를 맨 앞에 자동 삽입)
```

#### 생성되는 파일

```
docs/design/drafts/[feature-name]/
├── step1-architecture.md         ← 아키텍처 + 계층/패키지 + BCE→계층 매핑
├── step2-interactions.md         ← Use Case Realization + 시퀀스 다이어그램
├── step3-responsibilities.md     ← 책임 카탈로그 + GRASP 할당 + Controller 목록
├── step4-design-patterns.md      ← GoF 패턴 후보·채택·반증 표
├── step5-class-diagram.md        ← 클래스 상세(스테레오타입/가시성/시그니처) + 통합 DCD
├── step6-cross-cutting.md        ← Repository + 트랜잭션 경계 + 에러 정책 + 횡단 관심사
└── [feature-name]-design-draft.md ← 최종 통합본 (추적성 매트릭스 포함)
```

#### 단계별 확인 포인트

| 단계 | 확인할 내용 |
|------|-----------|
| 1단계 | 아키텍처 스타일이 OOA의 NFR과 외부 액터 수에 맞는가, BCE → 계층 매핑이 1:1로 추적 가능한가 |
| 2단계 | 모든 OOA UC가 Realization을 가지는가, participant 이름이 구체 클래스명인가, 1단계 의존 방향을 위반하지 않는가 |
| 3단계 | Information Expert가 데이터 소유 클래스에 배정되었는가, Bloated Controller(6 UC 이상)가 없는가 |
| 4단계 | 모든 채택 패턴이 OOA 근거와 반증 표를 가지는가, over-engineering이 아닌가 |
| 5단계 | 모든 클래스가 스테레오타입·패키지·`%% traced-from:` 주석을 가지는가, Step3의 단순 복제가 아닌가 |
| 6단계 | 모든 OOA 예외가 매핑되었는가, 모든 불허 전이가 가드/예외로 표현되었는가 |

---

### 5.8 ood-add-feature

기존 OOD 설계가 있는 프로젝트에 새로운 기능의 OOD를 추가합니다. **step0**(기존 OOD + 신규 OOA 분석)으로 시작한 뒤 6단계를 진행합니다.

#### 호출 예시

```
"기존 주문 OOD에 환불 기능 OOD를 추가해줘."
"refund 기능 클래스 설계 만들어줘 (기존 클래스 재사용해서)."
```

#### 전제 조건

**두 가지 입력**이 모두 필요합니다:
1. 기존 OOD: `docs/design/[project]-design.md` 또는 `docs/design/drafts/[기존-feature]/[기존-feature]-design-draft.md`
2. 신규 기능의 OOA: `docs/usecase/drafts/[새-feature]/[새-feature]-draft.md` 또는 메인 OOA 설계서에 신규 UC 병합 완료

#### ood-new-project와의 차이점

| 항목 | ood-new-project | ood-add-feature |
|------|----------------|-----------------|
| step0 | 없음 | 기존 OOD + 신규 OOA 동시 분석 (영향·재사용·신규 결정) |
| 클래스 ID·패키지 | 새로 정의 | 기존 재사용 |
| 다이어그램 표기 | 단일 색 | `%% NEW` / `%% EXTENDED` 주석으로 구분, 가능 시 색상 차별화 |
| 추적 주석 | UC·Step만 | 기존 UC + 신규 UC 모두 |
| 통합본 | 추적성 매트릭스만 | 매트릭스 + **변경 요약**(재사용/확장/신규 분류) |

---

### 5.9 ood-review

OOD 문서를 6개 관점에서 체계적으로 리뷰합니다.

#### 호출 예시

```
"order 기능 OOD 초안을 리뷰해줘."
"OOA 정합성만 집중적으로 봐줘."
"SOLID 원칙 검토 부탁해."
```

#### 리뷰 6개 관점

| 관점 | 검토 초점 |
|------|----------|
| **1. 완전성** | 6단계 파일 존재, 필수 표/Mermaid 존재, 모든 UC가 Realization 보유, 모든 도메인 엔티티가 DCD에 반영, **Step5가 Step3의 단순 복제가 아님** |
| **2. OOA 정합성 (추적성)** | 고아 클래스(OOA 근거 없음), 누락 UC, BCE→계층 매핑, 상태 모델 반영, 불허 전이→예외 매핑, 모든 OOA 예외 매핑, 변수 식별 반영 |
| **3. SOLID 준수** | SRP, OCP, LSP, ISP, DIP — 특히 Step1 의존 방향을 Step5가 위반하지 않는지 |
| **4. GRASP 적용 적절성** | Information Expert, Creator, Controller 적절성, **Bloated Controller 경고**(6 UC 이상), Low Coupling, High Cohesion |
| **5. 결합도·응집도·의존성 방향** | 계층 의존 방향 위반, 순환 의존, anemic domain, God Class, Pure Fabrication 남용 |
| **6. 디자인 패턴 적용 타당성** | **반증 표 존재**(없으면 CRITICAL), 패턴 역할 정확성, OOA 근거, over-engineering 경고 |

#### 생성되는 파일

```
docs/design/drafts/[feature]/review-report.md
```

#### 리뷰 후 선택지

uc-review와 동일한 3가지: **즉시 수정** / **확인만** / **부분 수정**.

OOD 리뷰 중 OOA 자체에 결함이 발견되면 ood-review가 **OOA부터 보강**할 것을 권고합니다 (uc-review로 우회).

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
        │   │   ├── step5-state-model.md
        │   │   ├── step6-system-boundary.md
        │   │   ├── step7-exceptions.md
        │   │   ├── step8-conditions.md
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

OOD까지 진행하면 `docs/design/`이 sibling으로 추가됩니다:

```
[project-root]/
└── docs/
    ├── usecase/                              ← OOA (위 구조)
    └── design/                               ← OOD (Phase 1)
        │
        ├── my-project-design.md              ← 메인 설계서 (Phase 2 ood-merge)
        ├── merge-report-2026-04-22.md        ← Phase 2
        │
        ├── drafts/
        │   ├── order/                        ← 1차 OOD 초안
        │   │   ├── step1-architecture.md
        │   │   ├── step2-interactions.md
        │   │   ├── step3-responsibilities.md
        │   │   ├── step4-design-patterns.md
        │   │   ├── step5-class-diagram.md
        │   │   ├── step6-cross-cutting.md
        │   │   ├── review-report.md
        │   │   └── order-design-draft.md
        │   │
        │   └── refund/                       ← 2차 OOD 초안 (ood-add-feature)
        │       ├── step0-existing-analysis.md  ← 기존 OOD + 신규 OOA 분석
        │       ├── step1-architecture.md
        │       ├── ...
        │       ├── step6-cross-cutting.md
        │       ├── review-report.md
        │       └── refund-design-draft.md
        │
        └── deprecated/                       ← Phase 2
```

---

## 7. 실전 시나리오별 가이드

### 시나리오 A: 프로젝트를 처음 시작할 때

```
1. "주문 관리 시스템 프로젝트를 시작하자. 유스케이스를 설계해줘."
   → uc-new-project 실행

2. 8단계 완료 후:
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

2. 8단계 완료 후:
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
   → usecase-driven-design 실행 (7단계)
```

### 시나리오 E: OOA를 OOD로 확장할 때

```
1. (OOA가 이미 완료된 상태)
   "OOA 끝났으니 이제 OOD 설계로 넘어가자."
   → ood-new-project 실행 (6단계)

2. 6단계 완료 후:
   "OOD 초안 리뷰해줘."
   → ood-review 실행 (6관점)

3. 리뷰 이슈 수정 후:
   (Phase 1에서는 OOD draft 단위로 사용. 메인 병합은 Phase 2 ood-merge 도입 후)
```

### 시나리오 F: 기존 OOD에 새 기능 설계 추가

```
1. (기존 OOD draft가 있고, 신규 기능의 OOA도 완료된 상태)
   "환불 기능 OOD를 추가해줘."
   → ood-add-feature 실행 (step0 분석 → 6단계 → 통합 초안)

2. "OOD 리뷰 부탁해."
   → ood-review 실행
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

- **소규모 프로젝트**, 빠른 프로토타이핑 → `usecase-driven-design` (7단계, Mermaid 없음)
- **중대규모 프로젝트**, 지속적 기능 추가 예정 → `uc-new-project` (8단계, 초안/메인 분리, Mermaid 포함)

### Q: 리뷰 없이 바로 병합해도 되나요?

가능합니다. `uc-merge`를 실행하면 리뷰를 권장하지만, 사용자가 원하면 바로 진행합니다.

### Q: 병합 후 초안 파일은 삭제해도 되나요?

삭제해도 동작에 문제는 없지만, 이력 추적을 위해 보존하는 것을 권장합니다. 병합된 초안은 상태가 `merged`로 변경되어 구분이 됩니다.

### Q: 한 번에 여러 기능의 초안을 만들 수 있나요?

네. `uc-add-feature`를 여러 번 실행하여 각각의 초안을 만든 뒤, `uc-merge`로 한 번에 병합할 수 있습니다.

### Q: 폐기한 UC를 되살릴 수 있나요?

- **소프트 폐기**한 경우: `[DEPRECATED]` 마킹을 제거하면 됩니다.
- **하드 제거**한 경우: `deprecated/` 폴더의 백업 파일을 참고하여 다시 추가합니다. `uc-add-feature`로 재추가하는 것을 권장합니다.

### Q: 상태 모델은 왜 필요한가요?

시나리오는 한 번의 실행 흐름을 기술하기 때문에, 하나의 엔티티가 여러 UC에 걸쳐 겪는 전체 생애주기를 조망할 수 없습니다. 상태 모델은 엔티티의 허용/불허 전이를 명시하여, 예외 정리(7단계)와 사전/사후조건(8단계)에서 상태 기반 검증 로직을 자연스럽게 도출할 수 있게 합니다.

### Q: OOD 없이 OOA만으로 구현해도 되나요?

가능합니다. OOA 산출물(특히 도메인 모델, 상태 모델, 사전/사후조건)만으로도 충분히 구현이 가능한 경우가 많습니다. OOD는 다음 상황에서 권장됩니다:

- **여러 개발자가 협업**하여 일관된 클래스 구조와 계층 의존이 필요할 때
- **장기 유지보수**가 예정되어 SOLID/GRASP 원칙 준수가 중요할 때
- **아키텍처 결정**(Hexagonal/Clean 등)을 명시적으로 문서화하고 싶을 때
- **디자인 패턴**(State, Strategy 등) 적용이 필요한 복잡한 도메인일 때

소규모 프로젝트이거나 빠른 프로토타이핑이라면 OOA만으로도 충분합니다.

### Q: OOD가 언어 무관이라고 하는데 실제 코드와는 어떻게 연결하나요?

OOD 산출물은 UML 일반 표기(`+ getName(): String`)로 작성되어 어떤 객체지향 언어로도 매핑할 수 있습니다. 코드 작성 시:

1. Step5의 클래스 상세 표를 보고 클래스/속성/메서드 시그니처를 1:1로 옮깁니다.
2. Step1의 패키지 구조를 디렉토리 구조로 만듭니다.
3. Step6의 트랜잭션 경계와 에러 정책을 application 서비스의 메서드에 적용합니다.
4. `%% traced-from:` 주석을 코드 주석이나 테스트 명세로 옮기면 OOA-OOD-코드 추적성이 유지됩니다.

언어별 코드 스켈레톤 자동 생성 스킬은 향후 별도로 검토 중입니다.

### Q: OOD Step3(GRASP)와 Step5(DCD)의 차이는 뭔가요?

둘 다 클래스 다이어그램을 만들지만 목적과 상세도가 다릅니다:

| 항목 | Step3 (GRASP 책임 할당) | Step5 (DCD) |
|------|----------------------|-------------|
| 목적 | "어떤 책임을 어느 클래스에 줄까?" 결정 | "이 설계로 코드를 짤 수 있는가?" 명세 확정 |
| 속성 | 없음 (메서드만 표시) | 가시성·타입 포함 완전 |
| 메서드 | 이름만 | 완전 시그니처 + 반환 |
| 관계 | 연관만 | 모든 UML 관계 (상속/합성/집약/구현/의존) |
| 스테레오타입 | 없음 | «entity»/«service»/«repository»/«controller» |

Step5는 Step3의 단순 복제가 아니라, **Step1의 계층 규칙과 Step4의 패턴 적용이 더해진 확장 결과**여야 합니다. ood-review 관점1이 "Step5가 Step3의 단순 복제인지"를 검사합니다.

### Q: ood-review에서 가장 흔한 CRITICAL은 무엇인가요?

경험상 다음 두 가지가 가장 흔합니다:

1. **고아 클래스** (관점 2: OOA 정합성) — Step5에 등장한 클래스가 `%% traced-from:` 주석이 없거나 OOA 어디에도 근거가 없는 경우. 해결: OOA 근거를 추가하거나, OOA에 빠진 책임이 있다면 uc-review로 OOA부터 보강.

2. **반증 없는 패턴 채택** (관점 6: 디자인 패턴 적용 타당성) — Step4에서 GoF 패턴을 채택했지만 "이 패턴 없이 풀 수 있는가?" 답변이 비어있는 경우. 해결: 반증을 채우거나, 반증이 약하면 패턴 제거.

### Q: OOD에 ood-merge가 없는 이유는 무엇인가요?

Phase 1에서는 의도적으로 제외했습니다. OOD 사용 패턴이 안정화된 뒤(=ood-new-project / ood-add-feature / ood-review가 충분히 검증된 뒤) Phase 2에서 도입할 예정입니다. 그동안 OOD는 draft 단위로 사용하고, 메인 통합이 필요하면 수동으로 진행합니다.
