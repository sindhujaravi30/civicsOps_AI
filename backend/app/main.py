from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.routes.chat import router as chat_router


app = FastAPI(
    title="CivicOps AI API",
    description=(
        "Backend API for the CivicOps AI "
        "government service assistant."
    ),
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/v1/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "civicops-api",
        "version": "1.0.0",
    }


app.include_router(chat_router)