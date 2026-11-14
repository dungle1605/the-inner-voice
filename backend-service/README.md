# 🛡️ Inner Voice - Backend Service (.NET 10 Clean Architecture)

> API Gateway và Tầng Nghiệp vụ cốt lõi (Core Business Logic) được xây dựng theo chuẩn **Clean Architecture** trên nền tảng **.NET 10 (C#)**, đảm bảo tính phân tách tuyệt đối giữa Domain, Application, Infrastructure và Web API.

---

## 🏛️ 1. Cấu trúc Clean Architecture

```
backend-service/
├── Domain/                                # 1. DOMAIN LAYER (Thuần C#, không phụ thuộc Framework ngoài)
│   ├── Entities/
│   │   └── ConversationLog.cs             # Thực thể lưu vết phiên hội thoại
│   ├── Enums/
│   │   └── RiskLevel.cs                   # Mức độ rủi ro (Low, Moderate, High, Critical)
│   └── Exceptions/
│       └── DomainException.cs             # Ngoại lệ miền nghiệp vụ
│
├── Application/                           # 2. APPLICATION USE CASES
│   ├── Common/Interfaces/
│   │   ├── IAppDbContext.cs               # Trừu tượng hóa truy cập CSDL
│   │   ├── IPiiAnonymizer.cs              # Trừu tượng hóa cơ chế ẩn danh GDPR
│   │   └── IPythonAiClient.cs             # Trừu tượng hóa kết nối sang Python AI
│   ├── DTOs/
│   │   └── ChatDtos.cs                    # Data Transfer Objects (Request, Response, Resource)
│   └── Services/
│       ├── IChatService.cs                # Use Case Interface
│       └── ChatService.cs                 # Xử lý Triage, PII Redaction, gọi AI và lưu CSDL
│
├── Infrastructure/                        # 3. INFRASTRUCTURE LAYER (Triển khai các Interface ngoài)
│   ├── Persistence/
│   │   └── AppDbContext.cs                # Triển khai EF Core 10 (SQLite)
│   └── Services/
│       ├── PiiAnonymizer.cs               # Lọc Regex email và số điện thoại theo chuẩn GDPR
│       └── PythonAiClient.cs              # Typed HttpClient gọi FastAPI với cơ chế Fallback
│
├── Controllers/                           # 4. PRESENTATION LAYER (Web API)
│   └── ChatController.cs                  # Mỏng (Thin Controller), chỉ ủy quyền cho IChatService
│
├── appsettings.json                       # Cấu hình CSDL và địa chỉ AI Microservice
├── Program.cs                             # IoC Dependency Injection và WebApplication Pipeline
└── Dockerfile                             # Multi-stage Container .NET 10
```

---

## 🔒 2. Tính năng Trọng tâm

1. **GDPR & HDS Data Privacy:** Mọi tin nhắn của vị thành niên đều đi qua [`PiiAnonymizer`](file:///g:/the-inner-voice/backend-service/Infrastructure/Services/PiiAnonymizer.cs) để che giấu email (`[EMAIL_REDACTED]`) và số điện thoại (`[PHONE_REDACTED]`) trước khi ghi vào CSDL.
2. **Crisis Intervention Guardrail:** Tự động phát hiện từ khóa nguy hiểm (tự hại/khủng hoảng) để kích hoạt thông điệp an toàn và số hotline khẩn cấp (Pháp: **3114** / Việt Nam: **111**).
3. **Data Pipeline Readiness (DP-800):** Cấu trúc bảng `ConversationLogs` chuẩn hóa, sẵn sàng tích hợp đồng bộ dữ liệu vào **Microsoft Fabric OneLake / Databricks**.

---

## 📡 3. API Endpoints

* `POST /api/chat`: Tiếp nhận tin nhắn, thực hiện nghiệp vụ và trả về kết quả.
* `GET /api/chat/history/{sessionId}`: Truy vấn lịch sử hội thoại đã ẩn danh.
* `GET /api/chat/emergency-resources`: Danh bạ cứu hộ khẩn cấp y tế cho trẻ vị thành niên.

---

## 💻 4. Khởi chạy phát triển (Local Development)

```powershell
cd backend-service
dotnet run
```
Dịch vụ sẽ khởi chạy tại `http://localhost:5000` (hoặc cổng HTTPS trong launchSettings.json).
Cơ sở dữ liệu SQLite `innervoice.db` sẽ tự động khởi tạo khi chạy lần đầu.
