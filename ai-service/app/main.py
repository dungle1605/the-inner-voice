from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.rag_engine import generate_response

app = FastAPI(title="Inner Voice AI Service")

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = []

@app.post('/api/chat')
async def chat_endpoint(request: ChatRequest):
    try:
        history_dict = [{"role": m.role, "content": m.content} for m in request.history]

        response_text = generate_response(request.message, chat_history=history_dict)
        return {"response": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "healthy"}