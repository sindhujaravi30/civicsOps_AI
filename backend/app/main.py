from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.routes.chat import router as chat_router
from backend.app.api.routes.documents import router as documents_router
from backend.app.db.session import init_db


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup: initializing database")
    try:
        await init_db()
    except Exception:
        logger.exception(
            "Application startup failed during database initialization"
        )
        raise

    logger.info("Application startup complete")
    try:
        yield
    finally:
        logger.info("Application shutdown")


app = FastAPI(
    title="CivicOps AI API",
    description=(
        "Backend API for the CivicOps AI "
        "government service assistant."
    ),
    version="1.0.0",
    lifespan=lifespan,
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
    logger.info("Health check request received")
    return {
        "status": "healthy",
        "service": "civicops-api",
        "version": "1.0.0",
    }


app.include_router(chat_router)
app.include_router(documents_router)