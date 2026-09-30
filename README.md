
# CivicOps AI

CivicOps AI is a bilingual government-service AI assistant designed as a portfolio project for exploring production AI engineering architecture.

The project focuses on:

- RAG
- Agentic workflows
- Tool calling
- Event-driven architecture
- PostgreSQL
- Redis
- Kafka
- AI evaluation
- Observability
- Kubernetes
- Model serving
- MCP

## Current milestone

### Milestone 2 — React/Vite UI

The project currently contains:

- FastAPI backend
- React frontend
- Vite development server
- Backend health API
- Frontend API integration
- CORS configuration
- Loading/error/healthy UI states
- Environment-based API configuration

## Architecture

```text
Browser
   |
   v
React + Vite
   |
   | HTTP
   v
FastAPI
   |
   v
Health API