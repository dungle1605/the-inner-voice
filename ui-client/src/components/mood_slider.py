from datetime import datetime
import streamlit as st

def render_mood_slider():
    st.subheader("📊 Check-in cảm xúc hôm nay")
    selected_mood = st.select_slider(
        "Bạn đang cảm thấy mức độ căng thẳng ra sao?",
        options=["Rất bình an", "Bình thường", "Hơi lo lắng", "Áp lực cao", "Quá tải"],
        value="Bình thường"
    )
    if st.button("Lưu cảm xúc vào nhật ký"):
        score_map = {"Rất bình an": 5, "Bình thường": 4, "Hơi lo lắng": 3, "Áp lực cao": 2, "Quá tải": 1}
        st.session_state.mood_history.append({
            "time": datetime.now().strftime("%H:%M"),
            "score": score_map[selected_mood],
            "mood": selected_mood
        })
        st.success("Đã ghi nhận cảm xúc của bạn!")
