"""적응형 라우팅: 프로젝트 규모에 따라 실행 전략을 자동 선택한다."""

from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass
class ProjectProfile:
    """프로젝트 규모/특성 프로파일."""

    estimated_uc_count: int = 5
    has_existing_docs: bool = False
    complexity: str = "medium"  # "simple" | "medium" | "complex"
    domains: list[str] = field(default_factory=list)


@dataclass
class ExecutionStrategy:
    """실행 전략."""

    workflow: str = "standard"       # "simplified" | "standard" | "domain_split"
    cost_tier: str = "standard"      # "economy" | "standard" | "premium"
    auto_merge: bool = True
    skip_review: bool = False
    domains: list[str] = field(default_factory=list)
    prompt_supplement: str = ""      # 오케스트레이터 프롬프트에 추가할 텍스트


# 복잡도 판단 키워드
_SIMPLE_KEYWORDS = [
    "간단한", "단순한", "하나의", "기본적인", "심플", "simple", "basic",
    "할일", "todo", "메모", "노트",
]
_COMPLEX_KEYWORDS = [
    "플랫폼", "시스템", "대규모", "여러 도메인", "종합", "통합",
    "이커머스", "e-commerce", "ERP", "CRM", "마켓플레이스",
    "platform", "enterprise", "complex",
]

# 도메인 추출 패턴
_DOMAIN_PATTERNS = [
    r"주문|결제|배송|회원|상품|재고|리뷰|쿠폰|정산|알림",
    r"인증|권한|사용자|프로필|설정|대시보드|통계|리포트",
    r"order|payment|shipping|member|product|inventory",
]


def analyze_request(user_prompt: str) -> ProjectProfile:
    """사용자 요청에서 프로젝트 규모를 추정한다."""
    prompt_lower = user_prompt.lower()

    # 복잡도 판단
    simple_score = sum(1 for kw in _SIMPLE_KEYWORDS if kw in prompt_lower)
    complex_score = sum(1 for kw in _COMPLEX_KEYWORDS if kw in prompt_lower)

    if simple_score > complex_score:
        complexity = "simple"
        estimated_uc = 3
    elif complex_score > simple_score:
        complexity = "complex"
        estimated_uc = 12
    else:
        complexity = "medium"
        estimated_uc = 6

    # 도메인 추출
    domains: list[str] = []
    for pattern in _DOMAIN_PATTERNS:
        matches = re.findall(pattern, user_prompt, re.IGNORECASE)
        domains.extend(matches)
    domains = list(dict.fromkeys(domains))  # 중복 제거, 순서 유지

    # 도메인이 많으면 복잡도 상향
    if len(domains) >= 4 and complexity != "complex":
        complexity = "complex"
        estimated_uc = max(estimated_uc, 10)

    return ProjectProfile(
        estimated_uc_count=estimated_uc,
        has_existing_docs=False,  # 실행 시 파일 존재 여부로 갱신
        complexity=complexity,
        domains=domains,
    )


def select_strategy(profile: ProjectProfile) -> ExecutionStrategy:
    """규모에 맞는 실행 전략을 반환한다."""
    if profile.complexity == "simple":
        return ExecutionStrategy(
            workflow="simplified",
            cost_tier="economy",
            auto_merge=True,
            skip_review=False,
            prompt_supplement=(
                "\n\n## 프로젝트 규모: 소규모\n\n"
                "이 프로젝트는 소규모입니다. 간소화된 워크플로우를 적용하세요:\n"
                "- UC 3개 이하로 간결하게 작성\n"
                "- Mermaid 다이어그램은 필수 최소만 (클래스 다이어그램, 상태 다이어그램)\n"
                "- 변수 식별은 핵심 변수만 (step 3 간소화)\n"
            ),
        )
    elif profile.complexity == "complex":
        domain_list = ", ".join(profile.domains) if profile.domains else "자동 식별"
        return ExecutionStrategy(
            workflow="domain_split",
            cost_tier="premium",
            auto_merge=False,  # 충돌 가능성 높아 수동 병합
            skip_review=False,
            domains=profile.domains,
            prompt_supplement=(
                f"\n\n## 프로젝트 규모: 대규모 (도메인: {domain_list})\n\n"
                "이 프로젝트는 대규모입니다. 도메인 분할 전략을 적용하세요:\n"
                f"- 식별된 도메인: {domain_list}\n"
                "- 도메인별로 기능을 그룹화하여 순차적으로 uc-new-project 또는 uc-add-feature를 실행\n"
                "- 각 도메인의 draft를 개별 리뷰한 후, 최종 통합 병합\n"
                "- 병합 시 도메인 간 엔티티 충돌에 주의\n"
                "- 병합 전 반드시 사용자에게 도메인 간 의존성을 확인받으세요\n"
            ),
        )
    else:
        return ExecutionStrategy(
            workflow="standard",
            cost_tier="standard",
            auto_merge=True,
            skip_review=False,
        )
