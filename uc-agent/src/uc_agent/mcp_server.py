"""MCP 서버: uc-agent를 MCP 도구로 노출한다.

Claude Code 또는 다른 MCP 클라이언트에서 UseCase 설계 기능을 도구로 호출할 수 있다.

사용법:
  uc-agent-mcp                # MCP 서버 실행
  # 또는
  python -m uc_agent.mcp_server
"""

from __future__ import annotations

import asyncio
import json
from typing import Any

try:
    from claude_agent_sdk import create_sdk_mcp_server, tool
    _HAS_SDK_MCP = True
except ImportError:
    _HAS_SDK_MCP = False

try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
    _HAS_MCP = True
except ImportError:
    _HAS_MCP = False


async def _collect_output(async_iter) -> str:
    """async iterator에서 텍스트를 수집한다."""
    texts: list[str] = []
    async for text in async_iter:
        texts.append(text)
    return "".join(texts)


# ---------------------------------------------------------------------------
# MCP 도구 구현 (SDK 또는 순수 MCP 패키지 사용)
# ---------------------------------------------------------------------------

if _HAS_SDK_MCP:
    # Claude Agent SDK의 내장 MCP 서버 사용
    @tool
    async def design_project(
        project_name: str,
        requirements: str,
        mode: str = "automated",
    ) -> str:
        """새 프로젝트의 UseCase를 설계한다.

        Args:
            project_name: 프로젝트 이름.
            requirements: 설계 요구사항.
            mode: 실행 모드 ("automated" 또는 "interactive").
        """
        from .orchestrator import run

        prompt = f"프로젝트명: {project_name}. {requirements}"
        return await _collect_output(run(prompt=prompt, mode=mode))

    @tool
    async def review_draft(draft_path: str) -> str:
        """UseCase 초안을 리뷰한다.

        Args:
            draft_path: 리뷰할 draft 파일 경로.
        """
        from .orchestrator import run_single_skill

        return await _collect_output(
            run_single_skill(
                skill_name="uc-review",
                prompt=f"{draft_path} 파일을 5개 관점으로 리뷰하세요.",
            )
        )

    @tool
    async def merge_draft(draft_path: str) -> str:
        """UseCase 초안을 메인 설계서에 병합한다.

        Args:
            draft_path: 병합할 draft 파일 경로.
        """
        from .orchestrator import run_single_skill

        return await _collect_output(
            run_single_skill(
                skill_name="uc-merge",
                prompt=f"{draft_path} 를 메인 설계서에 병합하세요.",
            )
        )

    @tool
    async def review_drafts_parallel(draft_paths: list[str]) -> str:
        """여러 UseCase 초안을 병렬로 리뷰한다.

        Args:
            draft_paths: 리뷰할 draft 파일 경로 목록.
        """
        from .parallel import parallel_review

        results = await parallel_review(draft_paths=draft_paths)
        lines = [f"병렬 리뷰 완료: {len(results)}건"]
        for r in results:
            cost_str = f" (${r.cost_usd:.4f})" if r.cost_usd else ""
            lines.append(f"  - {r.draft_path}{cost_str}")
        return "\n".join(lines)

    server = create_sdk_mcp_server(
        name="uc-design",
        tools=[design_project, review_draft, merge_draft, review_drafts_parallel],
    )

elif _HAS_MCP:
    # 순수 mcp 패키지 사용 (fallback)
    server = Server("uc-design")

    TOOLS = [
        Tool(
            name="design_project",
            description="새 프로젝트의 UseCase를 설계한다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_name": {"type": "string", "description": "프로젝트 이름"},
                    "requirements": {"type": "string", "description": "설계 요구사항"},
                    "mode": {"type": "string", "enum": ["automated", "interactive"], "default": "automated"},
                },
                "required": ["project_name", "requirements"],
            },
        ),
        Tool(
            name="review_draft",
            description="UseCase 초안을 리뷰한다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "draft_path": {"type": "string", "description": "리뷰할 draft 파일 경로"},
                },
                "required": ["draft_path"],
            },
        ),
        Tool(
            name="merge_draft",
            description="UseCase 초안을 메인 설계서에 병합한다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "draft_path": {"type": "string", "description": "병합할 draft 파일 경로"},
                },
                "required": ["draft_path"],
            },
        ),
    ]

    @server.list_tools()
    async def list_tools():
        return TOOLS

    @server.call_tool()
    async def call_tool(name: str, arguments: dict[str, Any]):
        if name == "design_project":
            from .orchestrator import run
            prompt = f"프로젝트명: {arguments['project_name']}. {arguments['requirements']}"
            result = await _collect_output(run(prompt=prompt, mode=arguments.get("mode", "automated")))
            return [TextContent(type="text", text=result)]

        elif name == "review_draft":
            from .orchestrator import run_single_skill
            result = await _collect_output(
                run_single_skill(skill_name="uc-review", prompt=f"{arguments['draft_path']} 파일을 리뷰하세요.")
            )
            return [TextContent(type="text", text=result)]

        elif name == "merge_draft":
            from .orchestrator import run_single_skill
            result = await _collect_output(
                run_single_skill(skill_name="uc-merge", prompt=f"{arguments['draft_path']} 를 병합하세요.")
            )
            return [TextContent(type="text", text=result)]

        return [TextContent(type="text", text=f"알 수 없는 도구: {name}")]

else:
    server = None


def main() -> None:
    """MCP 서버를 실행한다."""
    if server is None:
        print(
            "오류: MCP 서버를 실행하려면 claude-agent-sdk 또는 mcp 패키지가 필요합니다.\n"
            "  pip install claude-agent-sdk\n"
            "  또는\n"
            "  pip install mcp"
        )
        raise SystemExit(1)

    if _HAS_SDK_MCP:
        server.run()
    elif _HAS_MCP:
        asyncio.run(stdio_server(server))


if __name__ == "__main__":
    main()
