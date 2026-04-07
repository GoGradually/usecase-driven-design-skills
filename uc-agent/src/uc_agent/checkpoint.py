"""파이프라인 체크포인트 저장/로드."""

from __future__ import annotations

import glob as glob_mod
import json
import os
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone


CHECKPOINT_FILENAME = ".checkpoint.json"


@dataclass
class PipelineState:
    """파이프라인 실행 상태."""

    project_name: str = ""
    feature_name: str = ""
    mode: str = "automated"
    current_step: int = 1
    completed_steps: list[int] = field(default_factory=list)
    drafts_dir: str = ""
    original_prompt: str = ""
    created_at: str = ""
    updated_at: str = ""


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def save_checkpoint(state: PipelineState, drafts_dir: str) -> str:
    """체크포인트를 drafts_dir/.checkpoint.json에 저장한다.

    Returns:
        저장된 파일 경로.
    """
    state.drafts_dir = drafts_dir
    state.updated_at = _now_iso()
    if not state.created_at:
        state.created_at = state.updated_at

    checkpoint_path = os.path.join(drafts_dir, CHECKPOINT_FILENAME)
    os.makedirs(drafts_dir, exist_ok=True)

    with open(checkpoint_path, "w", encoding="utf-8") as f:
        json.dump(asdict(state), f, ensure_ascii=False, indent=2)

    return checkpoint_path


def load_checkpoint(drafts_dir: str) -> PipelineState | None:
    """체크포인트 파일을 로드한다. 없으면 None."""
    checkpoint_path = os.path.join(drafts_dir, CHECKPOINT_FILENAME)
    if not os.path.exists(checkpoint_path):
        return None

    with open(checkpoint_path, encoding="utf-8") as f:
        data = json.load(f)

    return PipelineState(**data)


def detect_progress(drafts_dir: str) -> int:
    """step 파일 존재 여부로 마지막 완료 step 번호를 추론한다.

    step1-*.md ~ step8-*.md 중 존재하는 마지막 번호를 반환.
    파일이 하나도 없으면 0을 반환.
    """
    if not os.path.isdir(drafts_dir):
        return 0

    last_step = 0
    for step_num in range(1, 9):
        pattern = os.path.join(drafts_dir, f"step{step_num}-*.md")
        matches = glob_mod.glob(pattern)
        if matches:
            # 파일이 비어있지 않은지 확인
            for match in matches:
                if os.path.getsize(match) > 0:
                    last_step = step_num
                    break

    return last_step


def mark_step_completed(drafts_dir: str, step_number: int) -> None:
    """특정 step을 완료로 표시한다. 체크포인트가 없으면 새로 생성."""
    state = load_checkpoint(drafts_dir)
    if state is None:
        state = PipelineState(drafts_dir=drafts_dir)

    if step_number not in state.completed_steps:
        state.completed_steps.append(step_number)
        state.completed_steps.sort()

    state.current_step = step_number + 1
    save_checkpoint(state, drafts_dir)
