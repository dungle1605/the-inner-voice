import streamlit as st
from src.services.backend_client import BackendApiClient

def render_chat_view(backend_client: BackendApiClient):
    st.subheader("🌱 Trò chuyện cùng Inner Voice")
    st.info("💡 Bạn có thể tự do tâm sự về áp lực học tập, bạn bè, gia đình hay bất cứ điều gì khiến bạn băn khoăn. Mình luôn ở đây lắng nghe mà không phán xét.")

    # Hiển thị toàn bộ lịch sử trò chuyện
    for msg in st.session_state.messages:
        avatar = "🌱" if msg["role"] == "assistant" else "👤"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])
            if msg.get("risk") == "Critical":
                st.warning("⚠️ Hệ thống đã tự động kích hoạt giao thức bảo vệ an toàn khẩn cấp.")

    # Hộp nhập tin nhắn
    user_input = st.chat_input("Hãy viết ra những gì bạn đang suy nghĩ...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_input)

        with st.chat_message("assistant", avatar="🌱"):
            with st.spinner("Inner Voice đang lắng nghe và suy ngẫm..."):
                history_payload = [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages[:-1]
                ]

                reply_text, risk_level, is_emergency = backend_client.send_chat_message(
                    session_id=st.session_state.session_id,
                    message=user_input,
                    history=history_payload
                )

                st.markdown(reply_text)
                if is_emergency:
                    st.error("🚨 Nếu bạn đang cảm thấy bế tắc, xin vui lòng gọi ngay Tổng đài 111 (VN) hoặc 3114 (Pháp). Bạn xứng đáng được giúp đỡ!")

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": reply_text,
                    "risk": risk_level
                })
