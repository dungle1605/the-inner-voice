# 🌱 Inner Voice - UI Client (Component-Based UI Architecture)

> Giao diện người dùng trên nền tảng **Streamlit**, được tái cấu trúc theo mô hình **Component & Service Architecture**, tách biệt hoàn toàn giữa Tầng Hiển thị (Views/Components), Tầng Quản lý Phiên (Session State) và Tầng Gọi API (Services).

---

## 🎨 1. Cấu trúc Mô-đun (Component-Based Structure)

```
ui-client/
├── src/
│   ├── models/
│   │   └── chat_models.py         # Kiểu dữ liệu ChatMessage, MoodRecord
│   ├── services/
│   │   ├── backend_client.py      # HTTP Client gọi .NET 10 (với fallback FastAPI)
│   │   └── session_manager.py     # Quản lý tập trung st.session_state
│   ├── components/                # Các UI Widgets tái sử dụng
│   │   ├── mood_slider.py         # Thanh trượt tự đánh giá căng thẳng
│   │   ├── breathing_exercise.py  # Widget hướng dẫn kỹ thuật thở 4-7-8
│   │   └── emergency_banner.py    # Banner cứu hộ khẩn cấp 111 (VN) và 3114 (Pháp)
│   └── views/                     # Các màn hình chính
│       ├── chat_view.py           # Không gian trò chuyện đồng cảm
│       └── analytics_view.py      # Bảng phân tích đồ thị cảm xúc (Fabric Demo)
│
├── app.py                         # Application Bootstrapper mỏng (chỉ nạp layout và views)
├── Dockerfile                     # Container Streamlit
└── requirements.txt               # streamlit, requests, plotly
```

---

## 💡 2. Trải nghiệm & Tính năng

* **Empathetic Chat Space:** Giao diện trò chuyện an toàn, hỗ trợ Markdown và các thông báo cảnh báo trực quan khi phát hiện rủi ro.
* **Mood Check-in & Grounding:** Tích hợp bài tập thở 4-7-8 giúp điều hòa hệ thần kinh khi lo âu cấp tính.
* **Fabric / Databricks Analytics Tab:** Trực quan hóa diễn biến chỉ số cân bằng cảm xúc bằng biểu đồ tương tác Plotly, mô phỏng việc khai thác dữ liệu từ **Gold Layer**.

---

## 💻 3. Khởi chạy phát triển (Local Development)

```powershell
cd ui-client
pip install -r requirements.txt
streamlit run app.py --server.port 8501
```
Giao diện sẽ mở tại trình duyệt: `http://localhost:8501`
