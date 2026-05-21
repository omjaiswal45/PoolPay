# PoolPay

A shared wallet / expense-pool API built with FastAPI, SQLAlchemy, and Celery.

## Stack

- **API** — FastAPI + Uvicorn
- **Database** — PostgreSQL via SQLAlchemy 2 + Alembic migrations
- **Auth** — JWT (python-jose) + bcrypt passwords
- **Background tasks** — Celery + Redis
- **AI** — OpenAI (pluggable via BaseAIProvider)

## Quick start

```bash
cp .env.example .env          # fill in your secrets
docker-compose up --build     # starts db, redis, api, worker
```

The API will be available at `http://localhost:8000`.  
Interactive docs: `http://localhost:8000/docs`

## Project structure

```
app/
  api/v1/       ← route handlers
  services/     ← business logic
  repositories/ ← database access
  models/       ← SQLAlchemy models
  schemas/      ← Pydantic schemas
  ai/           ← AI provider abstraction
  notifiers/    ← Email / SMS notifiers
  roles/        ← Role permission classes
  core/         ← Config, security, dependencies
  workers/      ← Celery background tasks
alembic/        ← Database migrations
tests/          ← Pytest test suite
```

## Running tests

```bash
pytest tests/
```
