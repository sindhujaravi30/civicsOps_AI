from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="CivicOps AI",
    version="1.0.0",
    description="Open-source AI government service assistant",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173",
        "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/v1/health")
def health():
    return {
        "status": "healthy",
        "service": "civicops-api",
        "version": "1.0.0",
    }