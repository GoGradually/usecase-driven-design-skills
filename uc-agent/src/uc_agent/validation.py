"""step 파일 검증 로직."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass

# step 파일별 필수 패턴
STEP_PATTERNS: dict[int, list[str]] = {
    1: [r"UC-\d+"],                           # UC ID가 하나 이상 존재
    2: [r"기본\s*흐름|기본흐름|Basic\s*Flow"],  # 기본 흐름 섹션
    3: [r"독립변수|Independent"],               # 변수 분류
    4: [r"엔티티|Entity|class\s"],             # 도메인 모델 엔티티
    5: [r"상태|State|stateDiagram"],            # 상태 모델
    6: [r"액터|Actor|시스템\s*경계|외부|내부"],   # 시스템 경계
    7: [r"예외|Exception|EX-"],                # 예외 정의
    8: [r"사전조건|사후조건|Precondition|Postcondition"],  # 조건
}


@dataclass
class ValidationResult:
    """검증 결과."""

    valid: bool
    file_path: str
    issues: list[str]

    def __str__(self) -> str:
        if self.valid:
            return f"✅ {self.file_path}"
        issues_str = "\n  - ".join(self.issues)
        return f"❌ {self.file_path}\n  - {issues_str}"


def validate_step_file(file_path: str, step_number: int | None = None) -> ValidationResult:
    """step 파일의 유효성을 검증한다.

    Args:
        file_path: 검증할 파일 경로.
        step_number: step 번호 (1-8). None이면 파일명에서 추출.

    Returns:
        ValidationResult.
    """
    issues: list[str] = []

    # 파일 존재 확인
    if not os.path.exists(file_path):
        return ValidationResult(valid=False, file_path=file_path, issues=["파일이 존재하지 않음"])

    # 파일 읽기
    with open(file_path, encoding="utf-8") as f:
        content = f.read()

    # 비어있는지 확인
    if not content.strip():
        return ValidationResult(valid=False, file_path=file_path, issues=["파일이 비어있음"])

    # 최소 길이 확인 (헤더만 있는 경우 방지)
    if len(content.strip()) < 50:
        issues.append("내용이 너무 짧음 (50자 미만)")

    # Step 헤더 확인
    if not re.search(r"#\s*(Step|단계)", content, re.IGNORECASE):
        issues.append("Step 헤더가 없음")

    # step 번호 추출
    if step_number is None:
        match = re.search(r"step(\d+)", os.path.basename(file_path), re.IGNORECASE)
        if match:
            step_number = int(match.group(1))

    # step별 특화 검증
    if step_number and step_number in STEP_PATTERNS:
        for pattern in STEP_PATTERNS[step_number]:
            if not re.search(pattern, content, re.IGNORECASE):
                issues.append(f"필수 패턴 누락: {pattern}")

    return ValidationResult(
        valid=len(issues) == 0,
        file_path=file_path,
        issues=issues,
    )


def validate_draft_file(file_path: str) -> ValidationResult:
    """통합 draft 파일의 유효성을 검증한다."""
    issues: list[str] = []

    if not os.path.exists(file_path):
        return ValidationResult(valid=False, file_path=file_path, issues=["파일이 존재하지 않음"])

    with open(file_path, encoding="utf-8") as f:
        content = f.read()

    if not content.strip():
        return ValidationResult(valid=False, file_path=file_path, issues=["파일이 비어있음"])

    # 주요 섹션 존재 확인
    required_sections = [
        (r"유스케이스|UseCase|UC-\d+", "유스케이스 목록"),
        (r"시나리오|Scenario|기본\s*흐름", "시나리오"),
        (r"도메인|Domain|엔티티|Entity", "도메인 모델"),
    ]

    for pattern, section_name in required_sections:
        if not re.search(pattern, content, re.IGNORECASE):
            issues.append(f"필수 섹션 누락: {section_name}")

    return ValidationResult(
        valid=len(issues) == 0,
        file_path=file_path,
        issues=issues,
    )


def validate_all_steps(drafts_dir: str) -> list[ValidationResult]:
    """drafts 디렉토리 내 모든 step 파일을 검증한다."""
    results: list[ValidationResult] = []

    for step_num in range(1, 9):
        file_path = os.path.join(drafts_dir, f"step{step_num}-*.md")
        # glob으로 매칭
        import glob as glob_mod

        matches = glob_mod.glob(file_path)
        if not matches:
            results.append(
                ValidationResult(
                    valid=False,
                    file_path=f"step{step_num}-*.md",
                    issues=[f"Step {step_num} 파일이 없음"],
                )
            )
        else:
            for match in matches:
                results.append(validate_step_file(match, step_num))

    return results
