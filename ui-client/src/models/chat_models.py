from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class ChatMessage:
    role: str
    content: str
    risk: str = "Low"
    timestamp: datetime = datetime.utcnow()

@dataclass
class MoodRecord:
    time: str
    score: int
    mood: str
