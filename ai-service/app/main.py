from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.routers.chat_router import router as chat_router
from app.api.v1.routers.health_router import router as health_router

def create_application() -> FastAPI:
    application = FastAPI(
        title="Inner Voice AI Microservice",
        description="Clean Architecture RAG & Adolescent Mental Health AI Platform (Azure Foundry & OpenAI)",
        version="2.0.0"
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Đăng ký các Router phiên bản hóa (v1)
    application.include_router(chat_router)
    application.include_router(health_router)

    return application

app = create_application()
