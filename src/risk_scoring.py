from typing import Dict, List


RISK_RULES = [
    {
        "label": "Unlimited liability exposure",
        "keywords": ["unlimited liability", "without limitation", "indemnify", "hold harmless"],
        "severity": "high",
        "score": 24,
        "reason": "The clause may create open-ended financial exposure.",
    },
    {
        "label": "Automatic renewal",
        "keywords": ["auto-renew", "automatic renewal", "renews automatically", "evergreen"],
        "severity": "medium",
        "score": 14,
        "reason": "The contract may continue unless terminated proactively.",
    },
    {
        "label": "Broad termination rights against you",
        "keywords": ["terminate at any time", "sole discretion", "without cause"],
        "severity": "high",
        "score": 18,
        "reason": "The other party may be able to exit with limited notice or justification.",
    },
    {
        "label": "Strict confidentiality obligations",
        "keywords": ["confidential", "non-disclosure", "proprietary information"],
        "severity": "medium",
        "score": 10,
        "reason": "Confidentiality duties can create compliance and operational risk.",
    },
    {
        "label": "Payment penalties",
        "keywords": ["late fee", "interest", "penalty", "liquidated damages"],
        "severity": "medium",
        "score": 12,
        "reason": "The clause introduces financial penalties for delay or breach.",
    },
    {
        "label": "Data protection commitments",
        "keywords": ["personal data", "data protection", "privacy", "security incident", "breach notification"],
        "severity": "medium",
        "score": 11,
        "reason": "Data handling terms may create legal and operational obligations.",
    },
    {
        "label": "Exclusivity restriction",
        "keywords": ["exclusive", "exclusivity", "non-compete"],
        "severity": "high",
        "score": 16,
        "reason": "The clause may restrict commercial flexibility.",
    },
]


def score_clauses(clauses: List[str]) -> Dict[str, object]:
    clause_results = []
    total_score = 0

    for index, clause in enumerate(clauses, start=1):
        lowered = clause.lower()
        hits = []
        clause_score = 0
        severity_rank = "low"

        for rule in RISK_RULES:
            if any(keyword in lowered for keyword in rule["keywords"]):
                hits.append(
                    {
                        "label": rule["label"],
                        "severity": rule["severity"],
                        "reason": rule["reason"],
                    }
                )
                clause_score += rule["score"]
                severity_rank = _max_severity(severity_rank, rule["severity"])

        if "shall" in lowered or "must" in lowered:
            clause_score += 4
            severity_rank = _max_severity(severity_rank, "medium")

        if "immediately" in lowered or "upon written notice" in lowered:
            clause_score += 3

        if clause_score == 0:
            severity_rank = "low"

        total_score += clause_score
        clause_results.append(
            {
                "clause_number": index,
                "text": clause,
                "score": min(clause_score, 100),
                "severity": severity_rank,
                "flags": hits,
            }
        )

    overall_score = min(total_score // max(len(clauses), 1), 100) if clauses else 0
    return {
        "overall_score": overall_score,
        "overall_severity": _severity_from_score(overall_score),
        "clauses": clause_results,
    }


def _max_severity(left: str, right: str) -> str:
    order = {"low": 0, "medium": 1, "high": 2}
    return left if order[left] >= order[right] else right


def _severity_from_score(score: int) -> str:
    if score >= 20:
        return "high"
    if score >= 10:
        return "medium"
    return "low"
