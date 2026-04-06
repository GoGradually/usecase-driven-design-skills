"""오케스트레이터: 멀티 에이전트 파이프라인 실행."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import AsyncIterator

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ResultMessage,
    TextBlock,
    query,
)

from .agents import build_agents

# 오케스트레이터 프롬프트 디렉토리
PROMPTS_DIR = Path(__file__).resolve().parent / "prompts"

# 오케스트레이터가 사용할 도구
ORCHESTRATOR_TOOLS = ["Read", "Glob", "Grep", "Agent", "Bash"]


def _load_prompt(mode: str) -> str:
    """모드별 오케스트레이터 프롬프트를 로드한다."""
    prompt_path = PROMPTS_DIR / f"orchestrator_{mode}.md"
    return prompt_path.read_text(encoding="utf-8")


async def run(
    *,
    prompt: str,
    mode: str = "interactive",
    cwd: str | None = None,
    skills_dir: str | None = None,
    model: str | None = None,
    worker_model: str | None = None,
    max_turns: int = 200,
) -> AsyncIterator[str]:
    """오케스트레이터를 실행하고 텍스트 출력을 스트리밍한다.

    Args:
        prompt: 사용자의 설계 요청.
        mode: "automated" 또는 "interactive".
        cwd: 프로젝트 루트 디렉토리. None이면 현재 디렉토리.
        skills_dir: SKILL.md 디렉토리. None이면 기본 경로.
        model: 오케스트레이터 모델. None이면 기본 모델.
        worker_model: 워커 에이전트 모델. None이면 부모 모델 상속.
        max_turns: 최대 에이전틱 턴 수.

    Yields:
        에이전트의 텍스트 응답 조각들.
    """
    orchestrator_prompt = _load_prompt(mode)
    agents = build_agents(skills_dir=skills_dir, model=worker_model)

    # interactive 모드에서는 AskUserQuestion 허용
    tools = list(ORCHESTRATOR_TOOLS)
    if mode == "interactive":
        tools.append("AskUserQuestion")

    options = ClaudeAgentOptions(
        system_prompt=orchestrator_prompt,
        model=model,
        allowed_tools=tools,
        agents=agents,
        max_turns=max_turns,
        permission_mode="acceptEdits",
    )

    session_id: str | None = None

    async for message in query(prompt=prompt, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    yield block.text
        elif isinstance(message, ResultMessage):
            session_id = message.session_id
            if message.total_cost_usd is not None:
                yield f"\n--- 완료 (비용: ${message.total_cost_usd:.4f}) ---\n"


async def run_single_skill(
    *,
    skill_name: str,
    prompt: str,
    cwd: str | None = None,
    skills_dir: str | None = None,
    model: str | None = None,
    max_turns: int = 50,
) -> AsyncIterator[str]:
    """단일 스킬을 직접 실행한다 (오케스트레이터 없이).

    Args:
        skill_name: 실행할 스킬 이름 (e.g., "uc-review").
        prompt: 작업 지시.
        cwd: 프로젝트 루트 디렉토리.
        skills_dir: SKILL.md 디렉토리.
        model: 사용할 모델.
        max_turns: 최대 에이전틱 턴 수.
    """
    from .agents import WORKER_TOOLS, load_skill_prompt, DEFAULT_SKILLS_DIR

    if skills_dir is None:
        skills_dir = DEFAULT_SKILLS_DIR

    skill_prompt = load_skill_prompt(skills_dir, skill_name)

    options = ClaudeAgentOptions(
        system_prompt=skill_prompt,
        model=model,
        allowed_tools=WORKER_TOOLS,
        max_turns=max_turns,
        permission_mode="acceptEdits",
    )

    async for message in query(prompt=prompt, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    yield block.text
        elif isinstance(message, ResultMessage):
            if message.total_cost_usd is not None:
                yield f"\n--- 완료 (비용: ${message.total_cost_usd:.4f}) ---\n"
