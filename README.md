# CivicOps AI

CivicOps AI is an early-stage project for an AI assistant focused on government services. The repository currently provides a minimal API health check and a local PostgreSQL/pgvector development service; the agent, retrieval, and service features are not implemented yet.

## Current Capabilities

- **API health check:** `GET /health` returns a healthy status for the `civicops-api` service.
- **Vector database service:** Docker Compose starts PostgreSQL 17 using the `pgvector/pgvector` image, exposes it on port `5432`, and persists database files in a named volume.
- **Backend structure:** Package directories are laid out for agents, API routes, core configuration, database access, evaluation, events, models, retrieval-augmented generation (RAG), services, and tools. These modules are currently placeholders.

Example health response:

```json
{
	"status": "healthy",
	"service": "civicops-api"
}
```

## Repository Layout

```text
backend/app/       FastAPI application and placeholder backend modules
data/              Data workspace
docker/            Docker-related files
frontend/          Frontend workspace
infrastructure/    Infrastructure workspace
knowledge_base/    Knowledge-base workspace
monitoring/        Monitoring workspace
src/civicsOps_AI/  Python package source workspace
tests/             Test workspace
chroma_db/         Local Chroma data workspace
docker-compose.yml Local PostgreSQL/pgvector service
pyproject.toml     Python project metadata
```

Most workspace directories are empty or contain only package initializers at this stage.

## Start the Database

Docker Desktop or another Docker Compose-compatible engine is required.

```powershell
docker compose up -d postgres
```

The development database is available on `localhost:5432` with the Compose defaults:

| Setting | Value |
| --- | --- |
| Database | `civicops` |
| Username | `civicops` |
| Password | `civicops` |

These credentials are for local development only. Stop the service with `docker compose down`; the named volume keeps database data across container stops. Removing the volume will delete that data.

## API Status

The FastAPI app is defined in `backend/app/main.py`. Its only route currently implemented is `GET /health`. The API dependencies are not declared in `pyproject.toml`, so FastAPI and an ASGI server such as Uvicorn must be installed separately before running it. For example, in an environment where they are installed:

```powershell
uvicorn backend.app.main:app --reload
```

Then visit `http://127.0.0.1:8000/health`.

## Project Metadata Note

The current `pyproject.toml` metadata still uses the name `workmate-ai` and points its console script at `workmate_ai:main`; that module and entry point are not present in this repository yet. The project currently has no automated tests or declared runtime dependencies.
