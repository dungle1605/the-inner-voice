import os
import streamlit as st
from src.services.session_manager import SessionManager
from src.services.backend_client import BackendApiClient
from src.components.mood_slider import render_mood_slider
from src.components.breathing_exercise import render_breathing_exercise
from src.components.emergency_banner import render_emergency_banner
from src.views.chat_view import render_chat_view
from src.views.analytics_view import render_analytics_view

# 1. Cấu hình trang
st.set_page_config(
    page_title="The Inner Voice | Tiếng Lòng Vị Thành Niên",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Khởi tạo trạng thái phiên (Session State)
SessionManager.initialize()

# 3. Khởi tạo Client giao tiếp Backend
dotnet_endpoint = os.getenv("BACKEND_URL", "http://localhost:5000/api/chat")
backend_client = BackendApiClient(dotnet_url=dotnet_endpoint)

# 4. Sidebar: Check-in cảm xúc, bài tập xoa dịu và hotline khẩn cấp
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/mental-health.png", width=120)
    st.title("The Inner Voice")
    st.caption("AI Đồng hành & Chăm sóc Sức khỏe Tâm thần Vị thành niên")
    st.divider()

    render_mood_slider()
    st.divider()

    render_breathing_exercise()
    render_emergency_banner()

# 5. Khung nhìn chính: Tabs giữa Trò chuyện và Nghiên cứu dữ liệu
tab_chat, tab_analytics = st.tabs(["💬 Không gian Trò chuyện", "📈 Bảng phân tích xu hướng (Fabric / Research Demo)"])

with tab_chat:
    render_chat_view(backend_client)

with tab_analytics:
    render_analytics_view()
