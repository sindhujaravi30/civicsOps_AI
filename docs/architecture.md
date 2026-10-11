# CivicOps AI Architecture

## Milestone 1

The initial architecture consisted of a stateless FastAPI backend.

```text
Client
  |
  v
FastAPI
  |
  v
Health Endpoint 

## Milestone 4 — PostgreSQL and SQLAlchemy

CivicOps AI now persists application data in PostgreSQL.

Architecture:

React + Vite
    |
FastAPI
    |
Chat Service
    |
SQLAlchemy
    |
PostgreSQL

Initial tables:

- conversations
- chat_messages
- service_requests

SQLAlchemy is used as the async ORM layer with asyncpg.

The application uses an async connection pool and explicit transaction
commit behavior.

PostgreSQL is currently used locally for development. The architecture
can later map to managed PostgreSQL infrastructure such as Azure
Database for PostgreSQL.

The current schema is intentionally minimal. Future milestones will
extend PostgreSQL for vector search, tool execution, audit records,
idempotency, and event-driven processing.