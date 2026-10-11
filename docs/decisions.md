## ADR-004: Use PostgreSQL with async SQLAlchemy

### Status

Accepted

### Context

CivicOps AI requires persistent relational storage for conversations,
messages, service requests, and future operational data.

The backend uses asynchronous FastAPI endpoints, so the database layer
should support asynchronous I/O.

### Decision

Use PostgreSQL as the primary relational database.

Use SQLAlchemy 2.x with its asynchronous API and asyncpg as the
PostgreSQL driver.

### Reasons

- Mature relational database
- ACID transactions
- Strong constraints
- Indexing support
- Connection pooling
- Async application compatibility
- Future pgvector support
- Suitable migration path to managed PostgreSQL

### Alternatives

SQLite:
Suitable for local prototypes but not the intended production
architecture.

MongoDB:
Flexible document storage, but relational constraints and transaction
semantics are more directly useful for the planned service workflow.

Separate vector database:
Will be reconsidered later. PostgreSQL plus pgvector can potentially
reduce infrastructure complexity.

### Trade-off

PostgreSQL introduces more operational complexity than an embedded
database, but it provides the relational consistency and extensibility
required for the target architecture.