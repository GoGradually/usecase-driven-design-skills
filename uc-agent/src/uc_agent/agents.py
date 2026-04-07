"""SKILL.md 로드 및 AgentDefinition 생성."""

from __future__ import annotations

import os
from pathlib import Path

from claude_agent_sdk import AgentDefinition

# 기본 스킬 디렉토리 (이 패키지 기준 상대 경로)
DEFAULT_SKILLS_DIR = str(
    Path(__file__).resolve().parent.parent.parent.parent
    / "usecase-driven-design"
    / "skills"
)

# 프롬프트 디렉토리
PROMPTS_DIR = Path(__file__).resolve().parent / "prompts"

# 워커 에이전트에 허용할 도구 목록
WORKER_TOOLS = ["Read", "Write", "Edit", "Glob", "Grep", "Bash"]

# 스킬별 기본 모델 티어 (작업 난이도 기반)
SKILL_MODEL_TIERS: dict[str, str] = {
    "uc-new-project": "sonnet",    # 생성 작업
    "uc-add-feature": "sonnet",    # 생성 작업
    "uc-review": "opus",           # 판단/분석 작업
    "uc-merge": "sonnet",          # 통합 작업
    "uc-deprecate": "opus",        # 영향 분석 작업
    "critic": "haiku",             # 경량 즉각 검사
}

# 비용 티어 프리셋
COST_TIER_PRESETS: dict[str, dict[str, str | None]] = {
    "economy": {"orchestrator": "sonnet", "worker_default": "haiku"},
    "standard": {"orchestrator": "opus", "worker_default": None},  # None = SKILL_MODEL_TIERS 사용
    "premium": {"orchestrator": "opus", "worker_default": "opus"},
}

# 스킬별 설명 (오케스트레이터가 어떤 에이전트를 선택할지 판단하는 데 사용)
SKILL_DESCRIPTIONS: dict[str, str] = {
    "uc-new-project": (
        "새 프로젝트의 UseCase 설계 초안을 8단계 워크플로우로 생성한다. "
        "프로젝트가 아직 없을 때 사용한다."
    ),
    "uc-add-feature": (
        "기존 프로젝트에 새 기능의 UseCase 초안을 추가한다. "
        "기존 메인 문서나 이전 초안이 있을 때 사용한다. "
        "docs/usecase/가 없고 소스 코드만 있는 경우에도 코드베이스 분석을 통해 사용할 수 있다."
    ),
    "uc-review": (
        "UseCase 초안 또는 메인 설계서를 6개 관점(완전성, 일관성, 품질, 구조, 문서간 정합성, 코드-설계 정합성)으로 리뷰한다. "
        "리뷰 리포트를 생성한다."
    ),
    "uc-merge": (
        "UseCase 초안(draft)을 메인 설계서에 병합한다. "
        "ID 재정렬, 도메인 모델 통합, 상태 모델 통합, 다이어그램 재생성을 수행한다."
    ),
    "uc-deprecate": (
        "UseCase를 폐기(deprecated 마킹) 또는 제거(문서에서 삭제)한다. "
        "7관점 영향 분석 후 연쇄 갱신한다."
    ),
}


def load_skill_prompt(skills_dir: str, skill_name: str) -> str:
    """SKILL.md를 읽어 YAML frontmatter를 제거한 본문을 반환한다."""
    skill_path = os.path.join(skills_dir, skill_name, "SKILL.md")
    with open(skill_path, encoding="utf-8") as f:
        content = f.read()

    # YAML frontmatter 제거 (--- ... ---)
    if content.startswith("---"):
        second_fence = content.index("---", 3)
        content = content[second_fence + 3 :].strip()

    return content


def _resolve_worker_model(
    skill_name: str,
    explicit_model: str | None,
    cost_tier: str | None,
) -> str | None:
    """워커 에이전트의 모델을 결정한다.

    우선순위: explicit_model > cost_tier preset > SKILL_MODEL_TIERS
    """
    if explicit_model is not None:
        return explicit_model

    if cost_tier is not None and cost_tier in COST_TIER_PRESETS:
        preset_default = COST_TIER_PRESETS[cost_tier]["worker_default"]
        if preset_default is not None:
            return preset_default

    return SKILL_MODEL_TIERS.get(skill_name)


def get_orchestrator_model(
    explicit_model: str | None = None,
    cost_tier: str | None = None,
) -> str | None:
    """오케스트레이터 모델을 결정한다."""
    if explicit_model is not None:
        return explicit_model
    if cost_tier is not None and cost_tier in COST_TIER_PRESETS:
        return COST_TIER_PRESETS[cost_tier]["orchestrator"]
    return None


def build_agents(
    skills_dir: str | None = None,
    model: str | None = None,
    cost_tier: str | None = None,
    project_dir: str | None = None,
) -> dict[str, AgentDefinition]:
    """워커 에이전트의 AgentDefinition dict를 생성한다.

    Args:
        skills_dir: SKILL.md 파일들이 위치한 디렉토리. None이면 기본 경로 사용.
        model: 워커 에이전트에 사용할 모델 (모든 스킬에 일괄 적용). None이면 티어별 자동 결정.
        cost_tier: 비용 티어 ("economy", "standard", "premium"). None이면 SKILL_MODEL_TIERS 사용.
        project_dir: 프로젝트 루트 디렉토리 (피드백 로드 등에 사용).
    """
    if skills_dir is None:
        skills_dir = DEFAULT_SKILLS_DIR

    # 피드백 로드 (프로젝트 디렉토리가 있는 경우)
    feedback_suffix = ""
    if project_dir is not None:
        from .feedback import load_feedback, build_feedback_prompt

        feedback_entries = load_feedback(project_dir)
        feedback_suffix = build_feedback_prompt(feedback_entries)
        if feedback_suffix:
            feedback_suffix = f"\n\n---\n\n## 과거 피드백 기반 주의사항\n\n{feedback_suffix}"

    agents: dict[str, AgentDefinition] = {}
    for skill_name, description in SKILL_DESCRIPTIONS.items():
        prompt = load_skill_prompt(skills_dir, skill_name)
        # 생성 에이전트에만 피드백 주입
        if feedback_suffix and skill_name in ("uc-new-project", "uc-add-feature"):
            prompt += feedback_suffix
        agent_model = _resolve_worker_model(skill_name, model, cost_tier)
        agents[skill_name] = AgentDefinition(
            description=description,
            prompt=prompt,
            tools=WORKER_TOOLS,
            model=agent_model,
        )

    # critic 에이전트 추가 (SKILL.md가 아닌 prompts/critic.md 사용)
    critic_prompt_path = PROMPTS_DIR / "critic.md"
    if critic_prompt_path.exists():
        agents["critic"] = AgentDefinition(
            description=(
                "생성된 step 파일의 CRITICAL 이슈를 즉시 검사하고 수정한다. "
                "UC ID 연속성, 주어 명시, 도메인 모델 일치, Mermaid 문법을 검사한다."
            ),
            prompt=critic_prompt_path.read_text(encoding="utf-8"),
            tools=WORKER_TOOLS,
            model=_resolve_worker_model("critic", model, cost_tier),
        )

    return agents
