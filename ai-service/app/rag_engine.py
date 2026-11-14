import asyncio
from typing import List, Dict, Any, Optional
from app.api.dependencies import get_mental_health_orchestrator
from app.domain.models import ChatMessage

def generate_response(message: str, chat_history: Optional[List[Dict[str, Any]]] = None) -> str:
    """
    Backward-compatible facade delegating to the Clean Architecture MentalHealthOrchestrator.
    """
    orchestrator = get_mental_health_orchestrator()
    domain_history = []
    if chat_history:
        for item in chat_history:
            domain_history.append(ChatMessage(
                role=item.get("role", "user"),
                content=item.get("content", "")
            ))

    # Chạy orchestrator async trong môi trường sync nếu được gọi trực tiếp
    loop = asyncio.new_event_loop()
    try:
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(
            orchestrator.process_chat(message=message, chat_history=domain_history)
        )
        return result.text
    finally:
        loop.close()
