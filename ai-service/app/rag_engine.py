import logging
from typing import List, Dict, Any, Optional
from app.config import settings
from app.azure_clients import get_openai_client, get_search_client

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """Bạn là "Inner Voice" - một trợ lý AI đồng hành và hỗ trợ tâm lý an toàn, ấm áp dành cho thanh thiếu niên (vị thành niên).

NGUYÊN TẮC HOẠT ĐỘNG VÀ ĐẠO ĐỨC AI (THEO TIÊU CHUẨN EU AI ACT & WHO):
1. LẮNG NGHE VÀ ĐỒNG CẢM: Luôn công nhận cảm xúc của người dùng ("Mình hiểu bạn đang cảm thấy...", "Thật khó khăn khi phải trải qua chuyện đó"). Không bao giờ phán xét hay hạ thấp cảm xúc của bạn trẻ.
2. GIỚI HẠN VAI TRÒ Y TẾ: Bạn KHÔNG PHẢI là bác sĩ tâm thần. Bạn KHÔNG BAO GIỜ chẩn đoán bệnh tâm thần (không tự ý gán nhãn như trầm cảm lâm sàng, rối loạn lưỡng cực) và TUYỆT ĐỐI KHÔNG kê đơn thuốc.
3. KHỦNG HOẢNG & TỰ HẠI: Nếu phát hiện bất kỳ dấu hiệu tự hại, muốn biến mất hoặc bế tắc cùng cực, lập tức thể hiện sự quan tâm an toàn và khuyên người dùng tìm kiếm sự trợ giúp khẩn cấp từ người lớn tin cậy hoặc đường dây nóng (Tổng đài 111 tại VN, 3114 tại Pháp).
4. KỸ NĂNG XOA DỊU (GROUNDING): Hướng dẫn các kỹ thuật điều hòa cảm xúc cơ bản và an toàn (như hít thở sâu 4-7-8, viết nhật ký cảm xúc, 5 giác quan).
5. NGÔN TỪ: Thân thiện, gần gũi, dịu dàng, phù hợp với lứa tuổi vị thành niên.
"""

def generate_response(message: str, chat_history: Optional[List[Dict[str, Any]]] = None) -> str:
    """
    Tạo phản hồi tâm lý an toàn sử dụng Azure OpenAI (GPT-4o-mini) và Azure AI Search (nếu có).
    """
    try:
        openai_client = get_openai_client()
        search_client = get_search_client()
        
        retrieved_context = ""
        # 1. Nếu có Azure AI Search, truy xuất tri thức tâm lý học chuẩn y khoa (RAG)
        if search_client:
            try:
                results = search_client.search(search_text=message, top=2)
                snippets = [doc.get("content", "") for doc in results if "content" in doc]
                if snippets:
                    retrieved_context = "\n---\nTài liệu tham khảo tâm lý bổ trợ:\n" + "\n".join(snippets) + "\n---\n"
            except Exception as se:
                logger.warning(f"Error querying Azure AI Search: {se}")

        # 2. Xây dựng chuỗi hội thoại
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]

        if retrieved_context:
            messages.append({"role": "system", "content": f"Sử dụng thông tin bổ trợ sau để trả lời nếu phù hợp:\n{retrieved_context}"})

        # Bổ sung lịch sử hội thoại gần nhất
        if chat_history:
            for item in chat_history[-6:]:
                role = item.get("role", "user")
                content = item.get("content", "")
                if role in ["user", "assistant"] and content:
                    messages.append({"role": role, "content": content})

        messages.append({"role": "user", "content": message})

        # 3. Gọi Azure OpenAI Model Deployment
        response = openai_client.chat.completions.create(
            model=settings.AZURE_OPENAI_MODEL_DEPLOYMENT_NAME,
            messages=messages,
            temperature=0.7,
            max_tokens=600
        )

        reply_content = response.choices[0].message.content
        return reply_content or "Mình luôn ở đây lắng nghe bạn, bạn có thể chia sẻ thêm được không?"

    except Exception as e:
        logger.error(f"Error in RAG generation: {e}")
        return (
            "Cảm ơn bạn đã tâm sự với mình. Dù hệ thống AI đang gặp chút gián đoạn kết nối, "
            "mình muốn bạn biết rằng cảm xúc của bạn rất quan trọng. "
            "Nếu bạn đang cảm thấy bế tắc, đừng ngần ngại chia sẻ với người thân hoặc liên hệ Tổng đài 111 (VN) / 3114 (Pháp) nhé."
        )
