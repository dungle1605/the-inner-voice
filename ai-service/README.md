# 🤖 Inner Voice - AI Microservice (Enterprise RAG Clean Architecture)

> Dịch vụ trí tuệ nhân tạo chuyên biệt hỗ trợ sức khỏe tâm thần vị thành niên, được thiết kế theo chuẩn **Clean Architecture** (tách bạch Domain, Protocols, Application, Infrastructure và API), tích hợp **Azure AI Foundry**, **Azure OpenAI (GPT-4o-mini)** và kỹ thuật **Hybrid RAG**.

---

## 🏗️ 1. Cấu trúc Clean Architecture

Khác với các mã nguồn prototype dạng flat-file, cấu trúc này tuân thủ nguyên lý **Dependency Inversion** (các module cấp cao không phụ thuộc module cấp thấp, cả hai cùng phụ thuộc vào Interface / Protocol):

```
ai-service/
├── app/
│   ├── core/                              # 1. CORE & DOMAIN FOUNDATIONS
│   │   ├── config.py                      # Cấu hình biến môi trường Azure
│   │   ├── exceptions.py                  # Domain Exceptions (AIException, SafetyPolicyViolationError)
│   │   └── prompts/
│   │       └── mental_health_prompts.py   # Mẫu System Prompt chuẩn y khoa (WHO/UNICEF)
│   │
│   ├── domain/                            # 2. DOMAIN SCHEMAS & PROTOCOLS (PEP 544)
│   │   ├── models.py                      # ChatMessage, RiskLevel, TriageAssessment, RetrievedSnippet
│   │   └── protocols.py                   # LLMProviderProtocol, VectorStoreProtocol
│   │
│   ├── application/                       # 3. APPLICATION USE CASES & ORCHESTRATION
│   │   ├── rag/
│   │   │   └── hybrid_retriever.py        # Dịch vụ truy xuất ngữ cảnh y khoa
│   │   ├── triage/
│   │   │   └── crisis_triage.py           # Phân loại rủi ro khẩn cấp (Crisis Evaluation)
│   │   └── services/
│   │       └── mental_health_orchestrator.py # Điều phối: Triage -> Retrieval -> Prompt -> Synthesis
│   │
│   ├── infrastructure/                    # 4. EXTERNAL ADAPTERS (Cụ thể hóa Protocols)
│   │   └── azure/
│   │       ├── openai_provider.py         # Triển khai LLMProviderProtocol qua AzureOpenAI SDK
│   │       └── search_provider.py         # Triển khai VectorStoreProtocol qua Azure AI Search
│   │
│   ├── api/                               # 5. PRESENTATION LAYER (FastAPI Web Interface)
│   │   ├── dependencies.py                # FastAPI Dependency Injection Container
│   │   └── v1/
│   │       ├── schemas.py                 # Pydantic DTOs cho API Request / Response
│   │       └── routers/
│   │           ├── chat_router.py         # POST /api/chat (Ủy quyền cho Orchestrator)
│   │           └── health_router.py       # GET /health
│   │
│   ├── rag_engine.py                      # Backward-compatible Facade
│   └── main.py                            # FastAPI Application Factory
│
├── Dockerfile                             # Container Python 3.11-slim
└── requirements.txt                       # Thư viện phụ thuộc
```

---

## 🛡️ 2. Đạo đức AI & Tiêu chuẩn Y khoa (EU AI Act & WHO)

* **Phân tầng Triage trước khi gọi LLM:** Trước khi gửi bất kỳ dữ liệu nào sang OpenAI, `CrisisTriageService` quét các biểu hiện tự hại / khủng hoảng. Nếu phát hiện rủi ro nghiêm trọng, hệ thống ngắt sinh văn bản tự do và kích hoạt thông điệp cứu trợ kèm hotline 3114 (Pháp) / 111 (Việt Nam).
* **Grounding (Chống ảo giác y khoa):** Kỹ thuật Hybrid RAG kết nối vào Azure AI Search để đưa các đoạn trích từ cẩm nang tâm lý học lâm sàng vào System Prompt.
* **Sliding Window Memory:** Quản lý lịch sử hội thoại trượt (tối đa 6 tin gần nhất) để tối ưu hóa latency và chi phí token.

---

## 📡 3. API Endpoints

| Method | Endpoint | Mô tả |
| :--- | :--- | :--- |
| `POST` | `/api/chat` | Tiếp nhận tin nhắn, thực hiện Triage và sinh phản hồi đồng cảm. |
| `GET` | `/health` | Kiểm tra trạng thái hoạt động của microservice. |
| `GET` | `/docs` | Swagger / OpenAPI UI tài liệu hóa tự động. |

---

## 💻 4. Khởi chạy phát triển (Local Development)

```powershell
cd ai-service
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000
```
Tài liệu Swagger tương tác mở tại: `http://localhost:8000/docs`
