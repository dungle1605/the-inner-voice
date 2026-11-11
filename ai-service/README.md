# 🤖 Inner Voice - AI Microservice (Python FastAPI)

> Dịch vụ trí tuệ nhân tạo chuyên biệt phục vụ hỗ trợ tâm lý vị thành niên, ứng dụng công nghệ **Azure AI Foundry**, **Azure OpenAI (GPT-4o-mini)** và kỹ thuật **Hybrid RAG (Retrieval-Augmented Generation)**.

---

## 🏗️ 1. Cấu trúc thư mục

```
ai-service/
├── app/
│   ├── __init__.py
│   ├── config.py           # Nạp biến môi trường từ .env (Azure endpoints, keys, models)
│   ├── azure_clients.py    # Factory khởi tạo AzureOpenAI (Managed Identity / API Key) & SearchClient
│   ├── rag_engine.py       # Lõi suy luận RAG, System Prompt đạo đức y tế & grounding
│   └── main.py             # FastAPI App expose các endpoint RESTful
├── scripts/                # Scripts tiện ích cho data ingestion / indexing
├── Dockerfile              # Container Python 3.11-slim chạy Uvicorn
└── requirements.txt        # Danh sách thư viện phụ thuộc
```

---

## 🛡️ 2. Đạo đức AI & System Prompt (WHO & EU AI Act Guidelines)

Toàn bộ phản hồi của mô hình được kiểm soát chặt chẽ bởi **System Prompt chuyên sâu về tâm lý vị thành niên**:
1. **Lắng nghe tích cực (Active Listening):** Công nhận và gọi tên cảm xúc, không phán xét, không hạ thấp trải nghiệm của trẻ.
2. **Không đóng vai bác sĩ (No Medical Diagnosis):** Tuyệt đối không tự ý chẩn đoán các bệnh lý tâm thần lâm sàng hoặc kê đơn thuốc.
3. **Kỹ thuật xoa dịu (Grounding Techniques):** Ưu tiên hướng dẫn các bài tập điều hòa cảm xúc an toàn (hít thở 4-7-8, viết nhật ký, chánh niệm đơn giản).
4. **Cơ chế phòng ngừa khủng hoảng (Crisis Protocol):** Tự động hướng dẫn trẻ kết nối tới các đường dây nóng hỗ trợ khẩn cấp nếu nhận thấy dấu hiệu bế tắc hoặc tự hại.

---

## ⚙️ 3. Biến môi trường cấu hình (`.env`)

Tạo hoặc cập nhật file `.env` ở thư mục gốc của repository:

```env
# Azure AI Foundry & OpenAI
PROJECT_ENDPOINT="https://<your-foundry-resource>.services.ai.azure.com/api/projects/<project-name>"
AZURE_OPENAI_ENDPOINT="https://<your-openai-resource>.openai.azure.com/"
AZURE_OPENAI_API_KEY="<your-azure-openai-key>"
AZURE_OPENAI_MODEL_DEPLOYMENT_NAME="gpt-4o-mini"
AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME="text-embedding-3-small"

# Azure AI Search (Tùy chọn cho tính năng RAG)
AZURE_SEARCH_ENDPOINT="https://<your-search-service>.search.windows.net"
AZURE_SEARCH_KEY="<your-search-admin-key>"
AZURE_SEARCH_INDEX_NAME="mental-health-index"
```

---

## 📡 4. Danh sách API Endpoints

### 1. `POST /api/chat`
Tiếp nhận tin nhắn người dùng và trả về phản hồi đồng cảm.
* **Request Body:**
  ```json
  {
    "message": "Dạo này mình cảm thấy rất áp lực chuyện thi cử và hay mất ngủ...",
    "history": [
      { "role": "user", "content": "Chào bạn" },
      { "role": "assistant", "content": "Chào bạn, mình luôn ở đây lắng nghe bạn..." }
    ]
  }
  ```
* **Response Body (200 OK):**
  ```json
  {
    "response": "Mình hiểu cảm giác áp lực thi cử có thể khiến bạn mệt mỏi thế nào..."
  }
  ```

### 2. `GET /health`
Kiểm tra trạng thái hoạt động của dịch vụ (Health Check).
* **Response Body (200 OK):**
  ```json
  { "status": "healthy" }
  ```

---

## 💻 5. Hướng dẫn cài đặt & Khởi chạy

### Cách 1: Sử dụng môi trường ảo Python cục bộ
```powershell
# 1. Di chuyển vào thư mục ai-service
cd ai-service

# 2. Tạo và kích hoạt môi trường ảo (nếu chưa có)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3. Cài đặt các thư viện phụ thuộc
pip install -r requirements.txt

# 4. Khởi động Uvicorn Server
uvicorn app.main:app --reload --port 8000
```
Tài liệu tương tác Swagger UI sẽ khả dụng tại: `http://localhost:8000/docs`

### Cách 2: Chạy bằng Docker
```bash
docker build -t inner-voice-ai-service .
docker run -p 8000:8000 --env-file ../.env inner-voice-ai-service
```

