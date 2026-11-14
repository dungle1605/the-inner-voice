import uuid
import streamlit as st
from typing import List, Dict, Any

class SessionManager:
    @staticmethod
    def initialize():
        if "session_id" not in st.session_state:
            st.session_state.session_id = str(uuid.uuid4())
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": "Chào bạn, mình là Inner Voice 🌱. Đây là không gian an toàn và bảo mật dành riêng cho bạn. Hôm nay bạn đang cảm thấy thế nào trong lòng?",
                    "risk": "Low"
                }
            ]
        if "mood_history" not in st.session_state:
            st.session_state.mood_history = [
                {"time": "08:00", "score": 3, "mood": "Bình thường"},
                {"time": "12:00", "score": 2, "mood": "Hơi lo âu"},
                {"time": "16:00", "score": 4, "mood": "Nhẹ nhõm hơn"},
            ]
