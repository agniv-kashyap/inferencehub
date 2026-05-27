# InferenceHub

## Distributed ML Infrastructure Platform

InferenceHub is a production-style distributed infrastructure platform that simulates how modern AI inference systems work internally.

Instead of running actual ML models, the platform focuses on:
- asynchronous task orchestration
- distributed worker systems
- API infrastructure
- authentication and authorization
- rate limiting
- workload orchestration
- persistent task lifecycle management

The project demonstrates backend and infrastructure engineering concepts commonly used in modern AI platforms.

---

# Features

- FastAPI API Gateway
- Redis Queue Broker
- Celery Distributed Workers
- PostgreSQL Persistence Layer
- Dockerized Microservices
- Async Task Processing
- API Key Authentication
- SHA256 API Key Hashing
- Redis Sliding Window Rate Limiting
- Free vs Premium Pipeline Authorization
- User Task History
- Persistent Task Lifecycle Management
- Multi-Tenant Architecture

---

# Architecture

```text
Client
   ↓
API Key Authentication
   ↓
Redis Rate Limiter
   ↓
Pipeline Authorization
   ↓
FastAPI Gateway
   ↓
PostgreSQL Task Persistence
   ↓
Redis Queue Broker
   ↓
Celery Workers
   ↓
Simulated ML Pipeline Execution
```

---

# Tech Stack

| Layer | Technology |
|---|---|
| API Framework | FastAPI |
| Background Workers | Celery |
| Queue Broker | Redis |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Validation | Pydantic |
| Containerization | Docker |
| Orchestration | Docker Compose |

---

# Available Pipelines

| Pipeline | Access |
|---|---|
| basic-document-summary | Free + Premium |
| enterprise-rag-analysis | Premium Only |

---

# API Endpoints

## Authentication

```text
POST /auth/keys
```

Generate developer API keys.

---

## Create Inference Task

```text
POST /infer
```

Headers:

```text
X-API-Key: sk_live_xxx
```

Request:

```json
{
  "pipeline": "basic-document-summary"
}
```

---

## Get Task By ID

```text
GET /tasks/{task_id}
```

---

## Get User Tasks

```text
GET /tasks
```

Returns all tasks belonging to the authenticated developer.

---

# Running the Project

## Start Services

```bash
docker-compose up --build
```

---

## Access Swagger Docs

```text
http://localhost:8000/docs
```

---

# Security Features

- SHA256 API key hashing
- Protected endpoints
- Tenant isolation
- Tier-based authorization
- Sliding window rate limiting
- User-specific task ownership

---

# Future Improvements

- Priority queues
- Worker autoscaling simulation
- Structured logging
- Flower monitoring
- WebSocket task updates
- Prometheus metrics
- Retry systems
- GPU scheduling simulation

---

# License

This project is intended for educational and infrastructure engineering demonstration purposes.

