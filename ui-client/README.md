# 🌱 Inner Voice - UI Client (Streamlit Frontend)

> Giao diện web thân thiện, nhẹ nhàng và an toàn dành riêng cho thanh thiếu niên, tích hợp đồng thời bảng điều khiển phân tích xu hướng cảm xúc phục vụ nghiên cứu khoa học.

---

## 🎨 1. Trải nghiệm Người dùng (UX Features)

1. **Không gian Trò chuyện Thân thiện (Empathetic Chat Space):**
   - Tông màu xanh mầm cây dịu mát, tạo cảm giác thư giãn và an toàn.
   - Trực tiếp giao tiếp với Backend **.NET 10** (tự động fallback sang Python AI nếu cần).
2. **Theo dõi Cảm xúc trong ngày (Daily Mood Tracker):**
   - Thanh trượt tự đánh giá mức độ căng thẳng (từ "Rất bình an" đến "Quá tải").
   - Ghi nhận lịch sử dao động cảm xúc theo các mốc thời gian trong ngày.
3. **Kỹ thuật thư giãn tích hợp (4-7-8 Breathing Grounding Exercise):**
   - Hướng dẫn thực hành hít thở sâu từng bước để giảm nhịp tim và kiểm soát cơn lo âu cấp tính.
4. **Cảnh báo khẩn cấp 1-Click (Emergency Hotlines):**
   - Luôn hiển thị sẵn sàng các số điện thoại hỗ trợ miễn phí 24/7 của Việt Nam (111, 096 306 1414) và Pháp (3114, 0 800 235 236).
5. **Tab Nghiên cứu Khoa học (Fabric / Research Demo):**
   - Trực quan hóa diễn biến tâm lý tổng hợp thông qua biểu đồ **Plotly**.
   - Minh họa luồng dữ liệu chuẩn bị đưa vào **Microsoft Fabric OneLake / Databricks** (tuân thủ mục tiêu DP-800).

---

## 📂 2. Cấu trúc thư mục

```
ui-client/
├── app.py              # Mã nguồn chính của ứng dụng Streamlit
├── requirements.txt    # streamlit, requests, plotly
└── Dockerfile          # Container Python chạy Streamlit trên cổng 8501
```

---

## 💻 3. Cài đặt & Khởi chạy

### Cách 1: Khởi chạy cục bộ
```powershell
# 1. Di chuyển vào thư mục ui-client
cd ui-client

# 2. Cài đặt thư viện
pip install -r requirements.txt

# 3. Khởi chạy Streamlit
streamlit run app.py --server.port 8501
```
Ứng dụng sẽ tự động mở tại trình duyệt: `http://localhost:8501`

### Cách 2: Khởi chạy bằng Docker
```bash
docker build -t inner-voice-ui .
docker run -p 8501:8501 -e BACKEND_URL=http://localhost:5000/api/chat inner-voice-ui
```

