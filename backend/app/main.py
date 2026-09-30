from fastapi import FastAPI

app = FastAPI(
    title="CivicOps AI",
    version="1.0.0",
    description="Open-source AI government service assistant",
)


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "civicops-api"
    }