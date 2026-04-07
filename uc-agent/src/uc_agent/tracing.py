"""파이프라인 옵저버빌리티 — 에이전트별 비용/시간 추적."""

from __future__ import annotations

import json
import os
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone


@dataclass
class AgentSpan:
    """단일 에이전트 실행 구간."""

    agent_name: str
    start_time: float = 0.0
    end_time: float | None = None
    cost_usd: float | None = None
    turns: int = 0
    status: str = "running"  # running | completed | failed

    @property
    def duration_sec(self) -> float:
        if self.end_time is None:
            return time.time() - self.start_time
        return self.end_time - self.start_time


class PipelineTracer:
    """파이프라인 전체의 실행 추적기."""

    def __init__(self) -> None:
        self.spans: list[AgentSpan] = []
        self._pipeline_start: float = time.time()

    def start_span(self, agent_name: str) -> AgentSpan:
        """새 에이전트 span을 시작한다."""
        span = AgentSpan(agent_name=agent_name, start_time=time.time())
        self.spans.append(span)
        return span

    def end_span(
        self,
        span: AgentSpan,
        *,
        cost: float | None = None,
        turns: int = 0,
        status: str = "completed",
    ) -> None:
        """span을 종료한다."""
        span.end_time = time.time()
        span.cost_usd = cost
        span.turns = turns
        span.status = status

    @property
    def total_cost(self) -> float:
        return sum(s.cost_usd for s in self.spans if s.cost_usd is not None)

    @property
    def total_duration(self) -> float:
        return time.time() - self._pipeline_start

    def summary(self) -> str:
        """파이프라인 실행 요약을 테이블 텍스트로 반환한다."""
        lines: list[str] = []
        lines.append("")
        lines.append("=== 파이프라인 실행 요약 ===")
        lines.append(f"{'에이전트':<20} {'시간':>8} {'비용':>10} {'상태':>6}")
        lines.append("-" * 48)

        for span in self.spans:
            dur = f"{span.duration_sec:.1f}s"
            cost = f"${span.cost_usd:.4f}" if span.cost_usd is not None else "-"
            status_icon = {"completed": "OK", "failed": "FAIL", "running": "..."}
            st = status_icon.get(span.status, span.status)
            lines.append(f"{span.agent_name:<20} {dur:>8} {cost:>10} {st:>6}")

        lines.append("-" * 48)
        lines.append(
            f"{'총합':<20} {self.total_duration:.1f}s"
            f"   ${self.total_cost:.4f}"
        )
        lines.append("")

        return "\n".join(lines)

    def save_report(self, output_dir: str) -> str:
        """추적 결과를 JSON 파일로 저장한다.

        Returns:
            저장된 파일 경로.
        """
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        filename = f".trace-{timestamp}.json"
        output_path = os.path.join(output_dir, filename)

        report = {
            "timestamp": timestamp,
            "total_duration_sec": self.total_duration,
            "total_cost_usd": self.total_cost,
            "spans": [
                {
                    "agent_name": s.agent_name,
                    "duration_sec": s.duration_sec,
                    "cost_usd": s.cost_usd,
                    "turns": s.turns,
                    "status": s.status,
                }
                for s in self.spans
            ],
        }

        os.makedirs(output_dir, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        return output_path
