from pydantic import BaseModel, Field
from typing import List, Optional

class ChatMessageDto(BaseModel):
    role: str = Field(..., description="Role của người gửi: 'user' hoặc 'assistant'")
    content: str = Field(..., description="Nội dung tin nhắn")

class ChatRequestDto(BaseModel):
    message: str = Field(..., min_length=1, description="Nội dung tâm sự của người dùng")
    history: Optional[List[ChatMessageDto]] = Field(default_factory=list, description="Lịch sử hội thoại")

class RetrievedSourceDto(BaseModel):
    title: str
    source: str
    relevance_score: float

class ChatResponseDto(BaseModel):
    response: str
    risk_level: str
    is_emergency: bool
    sources: List[RetrievedSourceDto] = []

class HealthStatusDto(BaseModel):
    status: str
    service: str = "ai-service"
    architecture: str = "Clean Architecture (Enterprise RAG)"
