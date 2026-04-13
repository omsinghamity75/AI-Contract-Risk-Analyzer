from typing import Dict, IO

from src.clause_splitter import split_into_clauses
from src.ner import extract_entities
from src.preprocess import extract_text
from src.risk_scoring import score_clauses


def analyze_contract(file: IO[bytes]) -> Dict[str, object]:
    text = extract_text(file)
    clauses = split_into_clauses(text)
    entities = extract_entities(text)
    risk_report = score_clauses(clauses)

    high_risk_clauses = [
        clause for clause in risk_report["clauses"] if clause["severity"] == "high"
    ]

    summary = _build_summary(entities, risk_report["overall_severity"], len(clauses))

    return {
        "text": text,
        "clause_count": len(clauses),
        "entities": entities,
        "risk_report": risk_report,
        "high_risk_clauses": high_risk_clauses,
        "summary": summary,
    }


def _build_summary(entities: Dict[str, object], overall_severity: str, clause_count: int) -> str:
    party_text = ", ".join(entities["parties"][:3]) if entities["parties"] else "No clear parties detected"
    amount_text = ", ".join(entities["amounts"][:2]) if entities["amounts"] else "no major payment amounts detected"
    return (
        f"Processed {clause_count} clauses. Overall risk is {overall_severity.upper()}. "
        f"Key parties: {party_text}. Financial references: {amount_text}."
    )
