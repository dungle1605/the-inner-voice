import logging
from typing import List, Optional
from app.domain.models import ChatMessage, AIResponseResult, TriageAssessment, RiskLevel
from app.domain.protocols import LLMProviderProtocol
from app.application.triage.crisis_triage import CrisisTriageService
from app.application.rag.hybrid_retriever import HybridRetrieverService
from app.core.prompts.mental_health_prompts import SYSTEM_EMPATHETIC_MENTAL_HEALTH, CRISIS_FALLBACK_MESSAGE

logger = logging.getLogger(__name__)

class MentalHealthOrchestrator:
    def __init__(
        self,
        llm_provider: LLMProviderProtocol,
        retriever: HybridRetrieverService,
        triage_service: CrisisTriageService
    ):
        self._llm = llm_provider
        self._retriever = retriever
        self._triage = triage_service

    async def process_chat(
        self,
        message: str,
        chat_history: Optional[List[ChatMessage]] = None
    ) -> AIResponseResult:
        # 1. Triage rủi ro khẩn cấp trước tiên (EU AI Act Safety Guardrail)
        assessment: TriageAssessment = self._triage.evaluate(message)
        if assessment.is_crisis:
            logger.warning(f"CRISIS DETECTED: Triggers={assessment.trigger_keywords}")
            return AIResponseResult(
                text=CRISIS_FALLBACK_MESSAGE,
                triage=assessment,
                retrieved_sources=[]
            )

        # 2. Truy xuất tri thức bổ trợ y khoa (RAG)
        retrieved_snippets = await self._retriever.retrieve_context(query=message, top_k=2)
        
        # 3. Chuẩn bị ngữ cảnh hội thoại
        messages: List[ChatMessage] = [
            ChatMessage(role="system", content=SYSTEM_EMPATHETIC_MENTAL_HEALTH)
        ]

        if retrieved_snippets:
            context_text = "\n---\nTài liệu tham khảo tâm lý bổ trợ:\n" + "\n".join(
                f"[{s.title}]: {s.content}" for s in retrieved_snippets
            ) + "\n---\n"
            messages.append(ChatMessage(
                role="system",
                content=f"Sử dụng thông tin bổ trợ sau để trả lời nếu phù hợp:\n{context_text}"
            ))

        # Sử dụng sliding window memory (tối đa 6 tin gần nhất)
        if chat_history:
            for item in chat_history[-6:]:
                if item.role in ["user", "assistant"] and item.content.strip():
                    messages.append(ChatMessage(role=item.role, content=item.content.strip()))

        messages.append(ChatMessage(role="user", content=message))

        # 4. Sinh phản hồi từ LLM
        try:
            reply_text = await self._llm.complete(messages=messages, temperature=0.7, max_tokens=600)
            if not reply_text.strip():
                reply_text = "Mình luôn ở đây lắng nghe bạn, bạn có thể chia sẻ thêm về điều này không?"
        except Exception as e:
            logger.error(f"Error executing LLM completion: {e}")
            reply_text = (
                "Cảm ơn bạn đã tâm sự với mình. Dù hệ thống AI đang gặp chút gián đoạn kỹ thuật, "
                "mình muốn bạn biết rằng cảm xúc của bạn rất quan trọng. "
                "Nếu bạn đang cảm thấy bế tắc, đừng ngần ngại chia sẻ với người thân hoặc liên hệ Tổng đài 111 (VN) / 3114 (Pháp) nhé."
            )

        return AIResponseResult(
            text=reply_text,
            triage=assessment,
            retrieved_sources=retrieved_snippets
        )
