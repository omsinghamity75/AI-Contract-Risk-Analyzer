import re
from typing import List


SECTION_BREAK_PATTERN = re.compile(
    r"(?=(?:\n\s*\d+(?:\.\d+)*[\).\s]+)|(?:\n\s*[A-Z][A-Z\s]{4,}:)|(?:\n\s*[A-Z][^\n]{0,80}\n))"
)


def split_into_clauses(text: str) -> List[str]:
    """Split contract text into reasonably sized clauses for downstream analysis."""
    normalized = re.sub(r"\r\n?", "\n", text or "")
    normalized = re.sub(r"[ \t]+", " ", normalized)
    normalized = re.sub(r"\n{3,}", "\n\n", normalized).strip()

    if not normalized:
        return []

    rough_sections = SECTION_BREAK_PATTERN.split(normalized)
    clauses: List[str] = []

    for section in rough_sections:
        chunk = section.strip()
        if not chunk:
            continue

        if len(chunk) <= 450:
            clauses.append(chunk)
            continue

        sentences = re.split(r"(?<=[.!?;])\s+(?=[A-Z0-9])", chunk)
        current = ""

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            candidate = f"{current} {sentence}".strip()
            if current and len(candidate) > 450:
                clauses.append(current.strip())
                current = sentence
            else:
                current = candidate

        if current:
            clauses.append(current.strip())

    return clauses
