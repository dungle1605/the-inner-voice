# 🛡️ Inner Voice - Backend Service (.NET 10 Web API)

> Cổng điều phối trung tâm (API Gateway & Core Service) được xây dựng trên nền tảng **.NET 10 (C#)**, đảm bảo tính an toàn dữ liệu theo tiêu chuẩn Châu Âu (**GDPR & HDS**) và quản lý cơ chế ứng phó khẩn cấp cho thanh thiếu niên (**Crisis Escalation**).

---

## 🏗️ 1. Cấu trúc thư mục

```
backend-service/
├── Controllers/
│   └── ChatController.cs        # Điều phối API chat, kích hoạt cứu hộ khẩn cấp & lịch sử
├── Data/
│   ├── AppDbContext.cs          # EF Core 10 DbContext cho SQLite
│   └── ConversationLog.cs       # Entity lưu trữ hội thoại đã được ẩn danh (Data pipeline cho Fabric)
├── Models/
│   ├── ChatMessage.cs           # DTO tin nhắn đơn lẻ
│   ├── ChatRequest.cs           # DTO tiếp nhận từ người dùng kèm SessionId
│   └── ChatResponse.cs          # DTO trả về kết quả kèm RiskLevel và Hotline khẩn cấp
├── Services/
│   ├── IPiiAnonymizer.cs        # Interface ẩn danh hóa dữ liệu cá nhân
│   ├── PiiAnonymizer.cs         # Triển khai lọc Regex số điện thoại, email
│   ├── IPythonAiClient.cs       # Interface gọi AI microservice
│   └── PythonAiClient.cs        # Typed HttpClient có resilience & fallback
├── appsettings.json             # Cấu hình Connection String và địa chỉ AI Service
├── InnerVoice.Api.csproj        # File dự án .NET 10
├── Program.cs                   # Khởi tạo DI, EF Core, OpenAPI và Middleware
└── Dockerfile                   # Multi-stage build container .NET 10
```

---

## 🔒 2. Tính năng Trọng tâm & Tuân thủ Chuẩn mực

### 1. Cơ chế bảo vệ khẩn cấp (Crisis & Self-Harm Escalation)
Khi phát hiện các dấu hiệu bế tắc cùng cực hoặc ý định tự hại (quét đa ngữ: tiếng Việt và tiếng Pháp), hệ thống sẽ:
* Đặt `RiskLevel = "Critical"` và `IsEmergency = true`.
* Tự động phản hồi thông điệp trấn an an toàn, không kích hoạt sinh văn bản tự do của AI để tránh rủi ro hallucination.
* Trả về ngay danh sách các đường dây nóng hỗ trợ khẩn cấp:
  - **Việt Nam:** Tổng đài Quốc gia Bảo vệ Trẻ em **111** (24/7, Miễn phí) / Tổng đài Ngày Mai **096 306 1414**.
  - **Pháp (France):** Numéro National Prévention Suicide **3114** (24/7, Gratuit) / Fil Santé Jeunes **0 800 235 236**.

### 2. Bảo mật & Ẩn danh hóa dữ liệu (GDPR / HDS Compliance)
* Trước khi lưu trữ nội dung vào cơ sở dữ liệu (`AppDbContext`), dịch vụ [`PiiAnonymizer`](file:///g:/the-inner-voice/backend-service/Services/PiiAnonymizer.cs) sẽ quét và thay thế toàn bộ địa chỉ email và số điện thoại bằng nhãn `[EMAIL_REDACTED]` và `[PHONE_REDACTED]`.
* Bảng dữ liệu `ConversationLogs` đã sẵn sàng để đồng bộ vào **Microsoft Fabric / Databricks OneLake (Bronze Layer)** phục vụ nghiên cứu khoa học mà không vi phạm quyền riêng tư.

---

## 📡 3. Danh sách API Endpoints

### 1. `POST /api/chat`
* **Request:**
  ```json
  {
    "sessionId": "b6a8d6f0-4596-4a1b-9eb0-a54133d1b827",
    "message": "Dạo này mình thấy rất bế tắc...",
    "history": []
  }
  ```
* **Response (200 OK):**
  ```json
  {
    "response": "Mình rất lo lắng cho bạn và muốn bạn được an toàn...",
    "riskLevel": "Critical",
    "isEmergency": true,
    "emergencyHotline": "VN: 111 / 1800 1567 | France: 3114 | Fil Santé Jeunes: 0 800 235 236",
    "timestamp": "2026-11-10T15:00:00Z"
  }
  ```

### 2. `GET /api/chat/history/{sessionId}`
Lấy lại toàn bộ lịch sử trò chuyện đã được ẩn danh của phiên làm việc.

### 3. `GET /api/chat/emergency-resources`
Truy xuất danh bạ các cơ sở y tế và đường dây nóng hỗ trợ tâm lý tại Việt Nam và Pháp.

---

## 💻 4. Cài đặt & Khởi chạy

### Yêu cầu môi trường:
* **.NET 10 SDK** (phiên bản `10.0.302` hoặc mới hơn).

### Khởi chạy:
```powershell
cd backend-service
dotnet restore
dotnet run
```
Dịch vụ sẽ lắng nghe tại cổng `http://localhost:5000` (hoặc cổng cấu hình trong `Properties/launchSettings.json`).
Cơ sở dữ liệu SQLite `innervoice.db` sẽ tự động được khởi tạo tại lần chạy đầu tiên.

