import re
from typing import Dict, List


MONEY_PATTERN = re.compile(
    r"(?:USD|INR|EUR|GBP|\$|Rs\.?)\s?\d[\d,]*(?:\.\d+)?(?:\s?(?:million|billion|crore|lakh))?",
    re.IGNORECASE,
)
DATE_PATTERN = re.compile(
    r"\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|"
    r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{2,4}|"
    r"\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\s+\d{2,4})\b",
    re.IGNORECASE,
)
PARTY_PATTERN = re.compile(
    r"\b(?:[A-Z][A-Za-z&,\-]+(?:\s+[A-Z][A-Za-z&,\-]+){0,4})\b"
)
OBLIGATION_PATTERN = re.compile(
    r"\b(shall|must|required to|agrees to|will not|may not)\b", re.IGNORECASE
)


def extract_entities(text: str) -> Dict[str, List[str]]:
    """Extract lightweight contract entities without requiring external models."""
    if not text:
        return {"parties": [], "dates": [], "amounts": [], "obligations": []}

    parties = _unique(
        match
        for match in PARTY_PATTERN.findall(text)
        if not _looks_like_heading(match) and len(match.split()) >= 2
    )
    dates = _unique(DATE_PATTERN.findall(text))
    amounts = _unique(MONEY_PATTERN.findall(text))
    obligations = _unique(
        sentence.strip()
        for sentence in re.split(r"(?<=[.!?])\s+", text)
        if OBLIGATION_PATTERN.search(sentence)
    )

    return {
        "parties": parties[:15],
        "dates": dates[:20],
        "amounts": amounts[:20],
        "obligations": obligations[:20],
    }


def _looks_like_heading(value: str) -> bool:
    words = value.split()
    return len(words) <= 5 and all(word.isupper() for word in words)


def _unique(values) -> List[str]:
    seen = set()
    output = []
    for value in values:
        cleaned = value.strip()
        key = cleaned.lower()
        if not cleaned or key in seen:
            continue
        seen.add(key)
        output.append(cleaned)
    return output
