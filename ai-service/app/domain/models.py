from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional

class RiskLevel(str, Enum):
    LOW = "Low"
    MODERATE = "Moderate"
    HIGH = "High"
    CRITICAL = "Critical"

@dataclass
class ChatMessage:
    role: str
    content: str
    timestamp: datetime = field(default_factory=datetime.utcnow)

@dataclass
class RetrievedSnippet:
    title: str
    content: str
    source: str = ""
    relevance_score: float = 0.0

@dataclass
class TriageAssessment:
    risk_level: RiskLevel
    is_crisis: bool
    trigger_keywords: List[str] = field(default_factory=list)
    confidence: float = 1.0

@dataclass
class AIResponseResult:
    text: str
    triage: TriageAssessment
    retrieved_sources: List[RetrievedSnippet] = field(default_factory=list)
