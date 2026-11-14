# 🌿 The Inner Voice (Tiếng Lòng)
### *Responsible AI & Multimodal Mental Health Platform for Adolescents*
> **An Enterprise Clean Architecture Ecosystem built with .NET 10, Python FastAPI (RAG Protocols), and Microsoft Fabric / Databricks (DP-800 Alignment).**  
> *Designed in strict compliance with the **EU AI Act** (High-Risk Healthcare Category) and **GDPR / French HDS** standards for European & French Academic Research Applications.*

---

## 📌 1. Giới thiệu dự án (Project Overview)

**The Inner Voice** là nền tảng số hỗ trợ và đồng hành chăm sóc sức khỏe tâm thần cho lứa tuổi thanh thiếu niên (vị thành niên). Dự án giải quyết bài toán cấp bách về khủng hoảng tâm lý học đường, áp lực đồng trang lứa và trầm cảm vị thành niên thông qua sự kết hợp giữa:
1. **Trí tuệ nhân tạo có trách nhiệm (Responsible AI):** Mô hình RAG (Retrieval-Augmented Generation) dựa trên cơ sở khoa học tâm lý (CBT - Liệu pháp Nhận thức Hành vi), tích hợp bộ lọc an toàn và cơ chế phản ứng khẩn cấp (Crisis Escalation).
2. **Kiến trúc Sạch (Clean Architecture) đồng bộ:** Phân tách rõ ràng giữa Core Domain, Use Cases (Application), External Adapters (Infrastructure) và Giao diện (Presentation) trên cả **.NET 10**, **Python FastAPI** và **Streamlit**.
3. **Kỹ thuật dữ liệu chuẩn mực (Data Engineering - DP-800):** Sẵn sàng tích hợp dữ liệu vào **Microsoft Fabric / Databricks** theo kiến trúc Medallion (Bronze - Silver - Gold) phục vụ nghiên cứu dịch tễ học sức khỏe tâm thần học đường.

---

## 🏛️ 2. Sơ đồ kiến trúc toàn hệ thống (System Architecture)

```mermaid
flowchart TB
    subgraph ClientLayer["🖥️ Frontend Tier (Component-Based UI)"]
        UI["Streamlit UI Client (Port 8501)\n- views/ (Chat & Analytics)\n- components/ (Mood, 4-7-8, Hotlines)\n- services/ (Session & API Client)"]
    end

    subgraph BackendLayer["🛡️ Core Backend Tier (.NET 10 Clean Architecture)"]
        WebAPI["WebApi / Controllers (Port 5000)"]
        AppLayer["Application Services\n- IChatService (Use Cases)\n- Common Interfaces (IAppDbContext, IPiiAnonymizer)"]
        DomainLayer["Domain Core\n- Entities (ConversationLog)\n- Enums (RiskLevel)\n- Domain Exceptions"]
        InfraLayer["Infrastructure Adapters\n- EF Core 10 (SQLite Persistence)\n- PiiAnonymizer (GDPR Redactor)\n- PythonAiClient (Resilient HTTP)"]
    end

    subgraph AILayer["🤖 AI Microservice Tier (Python Enterprise RAG)"]
        FastAPILayer["Presentation: FastAPI Routers (v1/chat, v1/health)"]
        Orchestrator["Application: MentalHealthOrchestrator\n- CrisisTriageService\n- HybridRetrieverService"]
        Protocols["Domain: Protocols & Schemas\n- LLMProviderProtocol\n- VectorStoreProtocol"]
        Providers["Infrastructure: Azure Providers\n- AzureOpenAIProvider (GPT-4o-mini)\n- AzureAISearchProvider"]
    end

    subgraph CloudLayer["☁️ Azure AI Cloud & Big Data Platform"]
        Foundry["Azure AI Foundry / Studio"]
        Search["Azure AI Search (Hybrid Vector Index)"]
        AOAI["Azure OpenAI Service"]
        Fabric[("Microsoft Fabric / Databricks OneLake\n(Bronze -> Silver -> Gold Analytics)")]
    end

    UI -->|"HTTP / REST API"| WebAPI
    WebAPI --> AppLayer
    AppLayer --> DomainLayer
    InfraLayer -. "Implements" .-> AppLayer
    InfraLayer -->|"Resilient HttpClient"| FastAPILayer

    FastAPILayer --> Orchestrator
    Orchestrator --> Protocols
    Providers -. "Implements" .-> Protocols
    Providers --> AOAI
    Providers -. "Retrieve Guidance" .-> Search
    Foundry -. "Governance & Tracing" .-> AOAI

    InfraLayer -. "ETL / Event Streaming" .-> Fabric
```

---

## 🔄 3. Quy trình tương tác & Luồng xử lý (End-to-End Workflow)

```mermaid
sequenceDiagram
    autonumber
    actor Teen as Vị thành niên (User)
    participant UI as UI Client (Streamlit Views)
    participant Net as .NET 10 Web API
    participant ChatSvc as IChatService (Application)
    participant AI as Python AI Orchestrator
    participant Azure as Azure OpenAI (Foundry)
    participant DB as AppDbContext (Logs)

    Teen->>UI: Gửi tâm sự ("Mình cảm thấy rất áp lực và mệt mỏi...")
    UI->>Net: POST /api/chat { sessionId, message, history }
    Net->>ChatSvc: HandleMessageAsync(request)
    
    rect rgb(240, 248, 255)
    Note over ChatSvc: Triage rủi ro khẩn cấp (EU AI Act)
    ChatSvc->>ChatSvc: Quét từ khóa tự hại / khủng hoảng
    alt Phát hiện nguy cơ khẩn cấp (Critical Self-Harm)
        ChatSvc-->>Net: Trả về hướng dẫn khẩn cấp + Hotlines (VN 111 / Pháp 3114)
    else An toàn (Low / Moderate Risk)
        ChatSvc->>AI: Gọi POST /api/chat (Python AI Microservice)
        AI->>AI: Kiểm tra Triage lớp 2 & nạp System Prompt y khoa
        AI->>Azure: Chat Completion (GPT-4o-mini + Knowledge Retrieval)
        Azure-->>AI: Phản hồi lắng nghe & gợi ý kỹ năng điều hòa cảm xúc
        AI-->>ChatSvc: JSON Response
    end
    end

    rect rgb(255, 250, 240)
    Note over ChatSvc,DB: Chuẩn GDPR / HDS Bảo vệ dữ liệu
    ChatSvc->>ChatSvc: Ẩn danh hóa PII (Loại bỏ Email, Số điện thoại)
    ChatSvc->>DB: Ghi log hội thoại đã ẩn danh vào CSDL
    end

    ChatSvc-->>Net: ChatResponseDto
    Net-->>UI: HTTP 200 OK
    UI-->>Teen: Hiển thị phản hồi ấm áp + Kỹ thuật xoa dịu (Grounding)
```

---

## 📂 4. Cấu trúc thư mục (Clean Architecture Repositories)

| Thư mục | Nền tảng | Kiến trúc triển khai | Tài liệu chi tiết |
| :--- | :--- | :--- | :--- |
| [**`backend-service/`**](./backend-service) | **.NET 10 (C#)** | **Clean Architecture**: Tách biệt `Domain`, `Application`, `Infrastructure`, `WebApi` (EF Core 10, PII Anonymizer, Typed HttpClient). | [Xem README](./backend-service/README.md) |
| [**`ai-service/`**](./ai-service) | **Python 3.11 / FastAPI** | **Enterprise RAG Architecture**: Tách biệt `core`, `domain/protocols`, `application/orchestrator`, `infrastructure/azure`, `api/v1`. | [Xem README](./ai-service/README.md) |
| [**`ui-client/`**](./ui-client) | **Streamlit / Plotly** | **Component-Based UI**: Tách biệt `components/`, `views/`, `services/`, `models/`. | [Xem README](./ui-client/README.md) |
| [**`docker-compose.yml`**](./docker-compose.yml) | Docker | Cấu hình triển khai trọn gói toàn bộ hệ thống bằng một câu lệnh duy nhất. | - |

---

## 🚀 5. Hướng dẫn khởi chạy nhanh (Quick Start)

### Cách 1: Khởi chạy trọn gói bằng Docker Compose (Khuyên dùng)
```bash
# Clone dự án và di chuyển vào thư mục gốc
cd the-inner-voice

# Xây dựng và khởi chạy cả 3 dịch vụ
docker-compose up --build
```
Sau khi khởi động thành công:
* **Giao diện người dùng (UI Client):** `http://localhost:8501`
* **Backend API (.NET 10 Swagger/OpenAPI):** `http://localhost:5000`
* **AI Microservice (FastAPI Docs):** `http://localhost:8000/docs`

---

### Cách 2: Khởi chạy thủ công từng dịch vụ (Development Mode)

#### 1. Khởi động AI Microservice (Python):
```powershell
cd ai-service
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000
```

#### 2. Khởi động Backend API (.NET 10):
```powershell
cd backend-service
dotnet run
```

#### 3. Khởi động UI Client (Streamlit):
```powershell
cd ui-client
streamlit run app.py --server.port 8501
```

---

## 🎓 6. Định hướng Nghiên cứu & Hồ sơ Học bổng Pháp (Academic Statement)

Dự án này được thiết kế có chủ đích nhằm đáp ứng các tiêu chí học thuật khắt khe khi ứng tuyển học bổng Thạc sĩ / Tiến sĩ tại Pháp (như Học bổng Eiffel, Viện nghiên cứu INRIA, CNRS, Paris-Saclay, Sorbonne, IP Paris):
1. **Tuân thủ EU AI Act:** Sức khỏe tâm thần vị thành niên thuộc nhóm *High-Risk AI Systems*. Dự án minh chứng khả năng thiết kế hệ thống có cơ chế kiểm soát của con người (*Human-in-the-loop*), giảm thiểu định kiến, và minh bạch nguồn tri thức tham chiếu.
2. **Bảo vệ quyền riêng tư y tế (GDPR & HDS Compliance):** Tích hợp tầng `PiiAnonymizer` độc lập để bảo đảm quyền riêng tư tuyệt đối cho trẻ em.
3. **Chuẩn bị dữ liệu lớn (DP-800 & Microsoft Fabric):** Kiến trúc dữ liệu phân tầng sẵn sàng cho nghiên cứu hành vi tâm lý diện rộng thông qua OneLake, Delta Lake và PySpark.
