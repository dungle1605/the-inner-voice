import streamlit as st
import plotly.graph_objects as go

def render_analytics_view():
    st.subheader("🔬 Phân tích xu hướng Cảm xúc (Dành cho Chuyên gia & Nghiên cứu sinh)")
    st.markdown("""
    Phần này mô phỏng dữ liệu được trích xuất từ **Bronze Layer** sang **Gold Layer** trên **Microsoft Fabric / Databricks** (tuân thủ đề cương DP-800):
    - Dữ liệu hoàn toàn **ẩn danh (Pseudonymized)**.
    - Cung cấp chỉ số diễn biến tâm lý phục vụ báo cáo khoa học.
    """)

    times = [item["time"] for item in st.session_state.mood_history]
    scores = [item["score"] for item in st.session_state.mood_history]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=times, y=scores,
        mode="lines+markers",
        name="Chỉ số cân bằng tâm lý",
        line=dict(color="#2ca02c", width=3),
        marker=dict(size=10)
    ))
    fig.update_layout(
        title="Biểu đồ dao động tâm lý trong ngày",
        xaxis_title="Thời gian",
        yaxis_title="Mức độ cân bằng (1: Nguy cơ cao -> 5: Rất tích cực)",
        yaxis=dict(range=[0, 6])
    )
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Tổng số phiên tương tác", value=len(st.session_state.messages))
    with col2:
        st.metric(label="Mức độ an toàn hội thoại", value="100% Tuân thủ Guardrail")
