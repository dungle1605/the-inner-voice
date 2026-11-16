# 🤖 Inner Voice - AI Microservice (Enterprise RAG Clean Architecture)

> Dịch vụ trí tuệ nhân tạo chuyên biệt hỗ trợ sức khỏe tâm thần vị thành niên, được thiết kế theo chuẩn **Clean Architecture** (tách bạch Domain, Protocols, Application, Infrastructure và API), tích hợp **Azure AI Foundry**, **Azure OpenAI (GPT-4o-mini)** và kỹ thuật **Hybrid RAG**.

---

## 🏗️ 1. Bản đồ cấu trúc thư mục (100% Khớp với Mã nguồn thực tế)

Toàn bộ mã nguồn trong thư mục `app/` được tổ chức thành 5 tầng rõ ràng theo nguyên lý **Dependency Inversion** (các module cấp cao không phụ thuộc module cấp thấp, cả hai cùng phụ thuộc vào Interface / Protocol):

```
ai-service/
├── Dockerfile                             # Container hóa Python 3.11-slim chạy Uvicorn
├── requirements.txt                       # Thư viện phụ thuộc (FastAPI, Azure SDKs, Pydantic)
├── app/
│   ├── main.py                            # FastAPI Application Factory & nạp Router
│   │
│   ├── core/                              # [TẦNG 1] NỀN TẢNG CẤU HÌNH & PROMPTS
│   │   ├── config.py                      # Nạp và quản lý biến môi trường từ .env
│   │   ├── exceptions.py                  # Domain Exceptions (AIException, LLMProviderError, ...)
│   │   └── prompts/
│   │       └── mental_health_prompts.py   # Mẫu System Prompt y khoa chuẩn WHO/UNICEF
│   │
│   ├── domain/                            # [TẦNG 2] MÔ HÌNH THỰC THỂ & PROTOCOLS (PEP 544)
│   │   ├── models.py                      # ChatMessage, RiskLevel, TriageAssessment, RetrievedSnippet
│   │   └── protocols.py                   # LLMProviderProtocol, VectorStoreProtocol (Trừu tượng hóa)
│   │
│   ├── infrastructure/                    # [TẦNG 3] KẾT NỐI HẠ TẦNG NGOÀI (AZURE CLOUD)
│   │   └── azure/
│   │       ├── openai_provider.py         # Triển khai LLMProviderProtocol bằng AzureOpenAI SDK
│   │       └── search_provider.py         # Triển khai VectorStoreProtocol bằng Azure AI Search
│   │
│   ├── application/                       # [TẦNG 4] USE CASES & ĐIỀU PHỐI NGHIỆP VỤ
│   │   ├── triage/
│   │   │   └── crisis_triage.py           # Bộ lọc an toàn quét từ khóa tự hại/khủng hoảng
│   │   ├── rag/
│   │   │   └── hybrid_retriever.py        # Truy xuất tài liệu tham khảo tâm lý học
│   │   └── services/
│   │       └── mental_health_orchestrator.py # Nhạc trưởng: Triage -> Retrieval -> Prompt -> Synthesis
│   │
│   └── api/                               # [TẦNG 5] PRESENTATION LAYER (REST API)
│       ├── dependencies.py                # Container Dependency Injection của FastAPI
│       └── v1/
│           ├── schemas.py                 # Pydantic DTOs (Request / Response validation)
│           └── routers/
│               ├── chat_router.py         # Endpoint POST /api/chat
│               └── health_router.py       # Endpoint GET /health
```

---

## 🛡️ 2. Nguyên lý Vận hành & Đạo đức AI (WHO & EU AI Act)

Mỗi tin nhắn gửi đến `POST /api/chat` sẽ trải qua chu trình xử lý nghiêm ngặt:

1. **Crisis Triage (Sàng lọc khẩn cấp):** [`crisis_triage.py`](file:///g:/the-inner-voice/ai-service/app/application/triage/crisis_triage.py) quét nội dung để phát hiện sớm nguy cơ tự hại hoặc khủng hoảng tâm lý (đa ngôn ngữ: tiếng Việt, tiếng Pháp, tiếng Anh). Nếu nguy cơ ở mức `Critical`, hệ thống **lập tức ngắt luồng gọi LLM** và trả về thông điệp cứu trợ kèm số hotline **3114 (Pháp)** / **111 (Việt Nam)** để đảm bảo an toàn tuyệt đối, tránh nguy cơ ảo giác.
2. **Hybrid Retrieval (Truy xuất tài liệu y khoa):** [`hybrid_retriever.py`](file:///g:/the-inner-voice/ai-service/app/application/rag/hybrid_retriever.py) truy vấn Azure AI Search để lấy các đoạn trích từ cẩm nang tâm lý chính thống nhằm làm giàu ngữ cảnh (Grounding).
3. **Sliding Window Memory (Bộ nhớ cửa sổ trượt):** [`mental_health_orchestrator.py`](file:///g:/the-inner-voice/ai-service/app/application/services/mental_health_orchestrator.py) giữ lại tối đa 6 lượt tin nhắn gần nhất để mô hình duy trì ngữ cảnh mà vẫn tiết kiệm chi phí token và giảm độ trễ (latency).
4. **Synthesis (Sinh phản hồi đồng cảm):** [`openai_provider.py`](file:///g:/the-inner-voice/ai-service/app/infrastructure/azure/openai_provider.py) gửi prompt đã được ghép hoàn chỉnh tới Azure OpenAI (`gpt-4o-mini`).

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
