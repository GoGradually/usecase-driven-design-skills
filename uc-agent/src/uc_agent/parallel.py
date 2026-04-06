"""병렬 리뷰 실행."""

from __future__ import annotations

from dataclasses import dataclass

import anyio

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ResultMessage,
    TextBlock,
    query,
)

from .agents import DEFAULT_SKILLS_DIR, WORKER_TOOLS, load_skill_prompt


@dataclass
class ReviewResult:
    """단일 draft 리뷰 결과."""

    draft_path: str
    report_text: str
    cost_usd: float | None = None


async def _review_single(
    draft_path: str,
    skills_dir: str,
    model: str | None,
) -> ReviewResult:
    """단일 draft를 리뷰하고 결과를 반환한다."""
    review_prompt = load_skill_prompt(skills_dir, "uc-review")

    texts: list[str] = []
    cost: float | None = None

    async for message in query(
        prompt=(
            f"{draft_path} 파일을 리뷰하세요. "
            "5개 관점 모두 검토하고 review-report.md를 생성하세요."
        ),
        options=ClaudeAgentOptions(
            system_prompt=review_prompt,
            model=model,
            allowed_tools=WORKER_TOOLS,
            max_turns=30,
            permission_mode="acceptEdits",
        ),
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    texts.append(block.text)
        elif isinstance(message, ResultMessage):
            cost = message.total_cost_usd

    return ReviewResult(
        draft_path=draft_path,
        report_text="\n".join(texts),
        cost_usd=cost,
    )


async def parallel_review(
    draft_paths: list[str],
    skills_dir: str | None = None,
    model: str | None = None,
) -> list[ReviewResult]:
    """여러 draft를 병렬로 리뷰한다.

    Args:
        draft_paths: 리뷰할 draft 파일 경로 목록.
        skills_dir: SKILL.md 디렉토리. None이면 기본 경로.
        model: 리뷰 에이전트 모델.

    Returns:
        각 draft의 ReviewResult 목록.
    """
    if skills_dir is None:
        skills_dir = DEFAULT_SKILLS_DIR

    results: list[ReviewResult] = []

    async with anyio.create_task_group() as tg:
        async def _do_review(path: str) -> None:
            result = await _review_single(path, skills_dir, model)
            results.append(result)

        for path in draft_paths:
            tg.start_soon(_do_review, path)

    return results
