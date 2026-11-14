from typing import List
from app.domain.models import RiskLevel, TriageAssessment

CRISIS_KEYWORDS = [
    # Tiếng Việt
    "tự tử", "muốn chết", "tự sát", "cắt tay", "kết liễu", "không muốn sống", "biến mất mãi mãi",
    # Tiếng Pháp
    "suicide", "me tuer", "en finir", "mourir", "automutilation", "mettre fin à mes jours",
    # Tiếng Anh
    "suicide", "kill myself", "end my life", "self-harm", "want to die"
]

class CrisisTriageService:
    def evaluate(self, user_message: str) -> TriageAssessment:
        normalized = user_message.lower().strip()
        matched_keywords: List[str] = [k for k in CRISIS_KEYWORDS if k in normalized]

        if matched_keywords:
            return TriageAssessment(
                risk_level=RiskLevel.CRITICAL,
                is_crisis=True,
                trigger_keywords=matched_keywords,
                confidence=0.98
            )

        return TriageAssessment(
            risk_level=RiskLevel.LOW,
            is_crisis=False,
            trigger_keywords=[],
            confidence=0.95
        )
