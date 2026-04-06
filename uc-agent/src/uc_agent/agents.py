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

# 워커 에이전트에 허용할 도구 목록
WORKER_TOOLS = ["Read", "Write", "Edit", "Glob", "Grep", "Bash"]

# 스킬별 설명 (오케스트레이터가 어떤 에이전트를 선택할지 판단하는 데 사용)
SKILL_DESCRIPTIONS: dict[str, str] = {
    "uc-new-project": (
        "새 프로젝트의 UseCase 설계 초안을 8단계 워크플로우로 생성한다. "
        "프로젝트가 아직 없을 때 사용한다."
    ),
    "uc-add-feature": (
        "기존 프로젝트에 새 기능의 UseCase 초안을 추가한다. "
        "기존 메인 문서나 이전 초안이 있을 때 사용한다."
    ),
    "uc-review": (
        "UseCase 초안 또는 메인 설계서를 5개 관점(완전성, 일관성, 품질, 구조, 문서간 정합성)으로 리뷰한다. "
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


def build_agents(
    skills_dir: str | None = None,
    model: str | None = None,
) -> dict[str, AgentDefinition]:
    """5개 워커 에이전트의 AgentDefinition dict를 생성한다.

    Args:
        skills_dir: SKILL.md 파일들이 위치한 디렉토리. None이면 기본 경로 사용.
        model: 워커 에이전트에 사용할 모델. None이면 부모 모델 상속.
    """
    if skills_dir is None:
        skills_dir = DEFAULT_SKILLS_DIR

    agents: dict[str, AgentDefinition] = {}
    for skill_name, description in SKILL_DESCRIPTIONS.items():
        prompt = load_skill_prompt(skills_dir, skill_name)
        agents[skill_name] = AgentDefinition(
            description=description,
            prompt=prompt,
            tools=WORKER_TOOLS,
            model=model,
        )

    return agents
