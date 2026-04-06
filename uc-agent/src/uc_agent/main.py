"""CLI 엔트리포인트."""

from __future__ import annotations

import argparse
import asyncio
import sys

from .agents import SKILL_DESCRIPTIONS


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="uc-agent",
        description="UseCase 설계 멀티 에이전트 시스템",
    )
    parser.add_argument(
        "prompt",
        nargs="?",
        help="설계 요청 (e.g., '주문 관리 시스템 설계')",
    )
    parser.add_argument(
        "--mode",
        choices=["automated", "interactive"],
        default="interactive",
        help="실행 모드 (기본: interactive)",
    )
    parser.add_argument(
        "--cwd",
        default=".",
        help="프로젝트 루트 디렉토리 (기본: 현재 디렉토리)",
    )
    parser.add_argument(
        "--skill",
        choices=list(SKILL_DESCRIPTIONS.keys()),
        help="단일 스킬 직접 실행 (오케스트레이터 우회)",
    )
    parser.add_argument(
        "--model",
        help="오케스트레이터 모델 (e.g., claude-opus-4-6)",
    )
    parser.add_argument(
        "--worker-model",
        help="워커 에이전트 모델 (e.g., claude-sonnet-4-6)",
    )
    parser.add_argument(
        "--max-turns",
        type=int,
        default=200,
        help="최대 에이전틱 턴 수 (기본: 200)",
    )
    parser.add_argument(
        "--skills-dir",
        help="SKILL.md 디렉토리 경로 (기본: 자동 감지)",
    )
    # 병렬 리뷰 서브커맨드
    parser.add_argument(
        "--parallel-review",
        nargs="+",
        metavar="DRAFT_PATH",
        help="여러 draft를 병렬로 리뷰 (e.g., --parallel-review draft1.md draft2.md)",
    )
    return parser


async def _run_orchestrator(args: argparse.Namespace) -> None:
    from .orchestrator import run

    if not args.prompt:
        print("오류: 설계 요청(prompt)을 입력해주세요.", file=sys.stderr)
        print("예시: uc-agent '주문 관리 시스템 설계'", file=sys.stderr)
        sys.exit(1)

    async for text in run(
        prompt=args.prompt,
        mode=args.mode,
        cwd=args.cwd,
        skills_dir=args.skills_dir,
        model=args.model,
        worker_model=args.worker_model,
        max_turns=args.max_turns,
    ):
        print(text, end="", flush=True)
    print()


async def _run_single_skill(args: argparse.Namespace) -> None:
    from .orchestrator import run_single_skill

    if not args.prompt:
        print(f"오류: {args.skill} 스킬에 전달할 prompt를 입력해주세요.", file=sys.stderr)
        sys.exit(1)

    async for text in run_single_skill(
        skill_name=args.skill,
        prompt=args.prompt,
        cwd=args.cwd,
        skills_dir=args.skills_dir,
        model=args.model,
        max_turns=args.max_turns,
    ):
        print(text, end="", flush=True)
    print()


async def _run_parallel_review(args: argparse.Namespace) -> None:
    from .parallel import parallel_review

    results = await parallel_review(
        draft_paths=args.parallel_review,
        skills_dir=args.skills_dir,
        model=args.worker_model or args.model,
    )

    print(f"\n=== 병렬 리뷰 완료: {len(results)}건 ===\n")
    total_cost = 0.0
    for result in results:
        print(f"📄 {result.draft_path}")
        if result.cost_usd:
            total_cost += result.cost_usd
            print(f"   비용: ${result.cost_usd:.4f}")
        print()
    if total_cost > 0:
        print(f"총 비용: ${total_cost:.4f}")


async def _async_main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    if args.parallel_review:
        await _run_parallel_review(args)
    elif args.skill:
        await _run_single_skill(args)
    else:
        await _run_orchestrator(args)


def main() -> None:
    """CLI 메인 함수."""
    asyncio.run(_async_main())


if __name__ == "__main__":
    main()
