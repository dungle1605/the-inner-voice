from fastapi import APIRouter, Depends, HTTPException
from app.api.v1.schemas import ChatRequestDto, ChatResponseDto, RetrievedSourceDto
from app.api.dependencies import get_mental_health_orchestrator
from app.application.services.mental_health_orchestrator import MentalHealthOrchestrator
from app.domain.models import ChatMessage

router = APIRouter(prefix="/api", tags=["Chat"])

@router.post("/chat", response_model=ChatResponseDto)
async def chat_endpoint(
    request: ChatRequestDto,
    orchestrator: MentalHealthOrchestrator = Depends(get_mental_health_orchestrator)
):
    try:
        domain_history = [
            ChatMessage(role=m.role, content=m.content)
            for m in (request.history or [])
        ]

        result = await orchestrator.process_chat(
            message=request.message,
            chat_history=domain_history
        )

        sources_dto = [
            RetrievedSourceDto(
                title=s.title,
                source=s.source,
                relevance_score=s.relevance_score
            )
            for s in result.retrieved_sources
        ]

        return ChatResponseDto(
            response=result.text,
            risk_level=result.triage.risk_level.value,
            is_emergency=result.triage.is_crisis,
            sources=sources_dto
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
