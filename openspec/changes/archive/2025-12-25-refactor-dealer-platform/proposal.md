# Change: Refactor to Dealer Ordering Platform

## Why

The current project is a simple order tracking demo using Vanilla JS frontend and JSON file storage. The business requires a full B2B dealer ordering platform with Vue 3 frontend, PostgreSQL database, and S3 image storage to support dealer management, product catalog, and order processing.

## What Changes

- **BREAKING**: Replace Vanilla JS frontend with Vue 3 + Vite + TypeScript
- **BREAKING**: Replace JSON file storage with PostgreSQL database (asyncpg)
- **BREAKING**: Update Docker Compose to include PostgreSQL service
- Add AWS S3 integration for image storage (boto3)
- Add Makefile with `up`, `dev`, `stop`, `db-init`, `db-migrate` commands
- Restructure backend with proper `app/` directory layout (routers, models, services, schemas)
- Add database migration infrastructure

## Scope (Phase 1 - Basic Structure)

This proposal focuses on getting the basic project structure runnable:
- [ ] Project directory structure
- [ ] Docker Compose with PostgreSQL
- [ ] Basic FastAPI app with asyncpg connection
- [ ] Basic Vue 3 + Vite frontend scaffold
- [ ] Makefile with required commands
- [ ] Database initialization script (schema only, no seed data)

Business logic and seed data will be added in subsequent phases.

## Impact

- Affected specs: `project-bootstrap` (major modifications)
- Affected code: `backend/`, `frontend/`, `docker-compose.yml`, new `Makefile`
- New dependencies: asyncpg, boto3, alembic (migrations), Vue 3, Vite, Pinia, Vue Router

## Out of Scope

- Business logic implementation (auth, products, orders, dealers)
- Seed data
- UI components and views
- Logging and monitoring (per user request)

