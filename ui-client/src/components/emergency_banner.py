import streamlit as st

def render_emergency_banner():
    st.error("🆘 **Hỗ trợ khẩn cấp 24/7 (Miễn phí)**")
    st.markdown("""
    **Việt Nam:**
    - 📞 **111**: Tổng đài Quốc gia Bảo vệ Trẻ em
    - 📞 **096 306 1414**: Đường dây nóng Ngày Mai

    **Pháp (France):**
    - 📞 **3114**: Prévention du Suicide (24/7)
    - 📞 **0 800 235 236**: Fil Santé Jeunes
    """)
    st.divider()
    st.caption("🔒 **Cam kết GDPR & HDS**: Mọi tin nhắn đều được ẩn danh hóa tự động trước khi lưu trữ. Không lưu thông tin định danh cá nhân.")
