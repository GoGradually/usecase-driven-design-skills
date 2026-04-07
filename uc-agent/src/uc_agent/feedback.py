"""피드백 루프: 리뷰 패턴을 수집하여 다음 생성에 반영한다."""

from __future__ import annotations

import json
import os
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone


FEEDBACK_FILENAME = ".feedback-history.json"


@dataclass
class FeedbackEntry:
    """단일 피드백 항목."""

    timestamp: str = ""
    skill: str = ""
    issue_type: str = ""       # "CRITICAL" | "WARNING"
    pattern: str = ""          # 예: "시나리오 step에 주어 누락"
    frequency: int = 1         # 동일 패턴 발생 횟수


def _feedback_path(project_dir: str) -> str:
    return os.path.join(project_dir, "docs", "usecase", FEEDBACK_FILENAME)


def load_feedback(project_dir: str) -> list[FeedbackEntry]:
    """프로젝트의 피드백 히스토리를 로드한다."""
    path = _feedback_path(project_dir)
    if not os.path.exists(path):
        return []

    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    return [FeedbackEntry(**entry) for entry in data]


def save_feedback(project_dir: str, entries: list[FeedbackEntry]) -> str:
    """피드백 히스토리를 저장한다.

    Returns:
        저장된 파일 경로.
    """
    path = _feedback_path(project_dir)
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump([asdict(e) for e in entries], f, ensure_ascii=False, indent=2)

    return path


def extract_patterns_from_review(review_report_path: str) -> list[FeedbackEntry]:
    """리뷰 리포트에서 CRITICAL/WARNING 패턴을 추출한다.

    리뷰 리포트의 마크다운 구조에서 이슈를 파싱한다:
    - ### [CRITICAL] ... 또는 ### [WARNING] ... 섹션
    - 각 번호 항목을 하나의 패턴으로 추출
    """
    if not os.path.exists(review_report_path):
        return []

    with open(review_report_path, encoding="utf-8") as f:
        content = f.read()

    entries: list[FeedbackEntry] = []
    now = datetime.now(timezone.utc).isoformat()

    # [CRITICAL] 또는 [WARNING] 섹션 내 번호 항목 추출
    current_type: str | None = None
    for line in content.splitlines():
        # 섹션 헤더 감지
        critical_match = re.match(r"#+\s*\[?(CRITICAL|WARNING)\]?", line, re.IGNORECASE)
        if critical_match:
            current_type = critical_match.group(1).upper()
            continue

        # 다른 섹션 시작 시 리셋
        if re.match(r"#+\s", line) and current_type:
            current_type = None
            continue

        # 번호 항목 추출
        if current_type:
            item_match = re.match(r"\s*\d+\.\s+(.+)", line)
            if item_match:
                pattern_text = item_match.group(1).strip()
                # 너무 긴 텍스트는 앞 100자로 자름
                if len(pattern_text) > 100:
                    pattern_text = pattern_text[:100] + "..."
                entries.append(
                    FeedbackEntry(
                        timestamp=now,
                        skill="uc-review",
                        issue_type=current_type,
                        pattern=pattern_text,
                        frequency=1,
                    )
                )

    return entries


def merge_feedback(
    existing: list[FeedbackEntry],
    new_entries: list[FeedbackEntry],
) -> list[FeedbackEntry]:
    """기존 피드백에 새 항목을 병합한다. 동일 패턴이면 frequency를 증가."""
    # 패턴을 키로 사용하여 기존 항목 인덱싱
    pattern_map: dict[str, FeedbackEntry] = {}
    for entry in existing:
        pattern_map[entry.pattern] = entry

    for new_entry in new_entries:
        if new_entry.pattern in pattern_map:
            pattern_map[new_entry.pattern].frequency += 1
            pattern_map[new_entry.pattern].timestamp = new_entry.timestamp
        else:
            pattern_map[new_entry.pattern] = new_entry

    # frequency 내림차순 정렬
    return sorted(pattern_map.values(), key=lambda e: e.frequency, reverse=True)


def build_feedback_prompt(entries: list[FeedbackEntry], top_n: int = 5) -> str:
    """빈도 상위 N개 패턴을 프롬프트 보충 텍스트로 변환한다.

    Returns:
        프롬프트에 추가할 텍스트. 피드백이 없으면 빈 문자열.
    """
    if not entries:
        return ""

    # 상위 N개만 사용
    top_entries = entries[:top_n]

    lines = ["과거 리뷰에서 반복 지적된 사항입니다. 이 사항들을 특히 주의하여 작성하세요:\n"]
    for i, entry in enumerate(top_entries, 1):
        type_icon = "CRITICAL" if entry.issue_type == "CRITICAL" else "WARNING"
        lines.append(f"{i}. [{type_icon}] {entry.pattern} ({entry.frequency}회 반복)")

    return "\n".join(lines)
