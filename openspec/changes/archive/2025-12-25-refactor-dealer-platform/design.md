## Context

Refactoring from a simple demo project to a production-ready B2B dealer ordering platform. This involves complete technology stack changes for both frontend and backend.

## Goals / Non-Goals

### Goals
- Establish runnable project structure with new tech stack
- PostgreSQL database with migration support
- Vue 3 + Vite frontend scaffold
- Makefile for common operations
- S3 configuration ready (not fully implemented yet)

### Non-Goals
- Business logic implementation (Phase 2)
- Seed data (Phase 2)
- Full UI implementation (Phase 2)
- Logging/monitoring infrastructure

## Decisions

### Database: PostgreSQL with asyncpg

**Decision**: Use asyncpg for async PostgreSQL access
**Why**: FastAPI is async-native; asyncpg provides best performance for async Python PostgreSQL access
**Alternatives**: psycopg2 (sync), SQLAlchemy async (heavier abstraction)

### Frontend: Vue 3 + Vite + TypeScript

**Decision**: Vue 3 Composition API with Vite build tool
**Why**: Modern, fast development experience, TypeScript support, good ecosystem
**Alternatives**: React (larger ecosystem but more complex), Nuxt (SSR not needed)

### State Management: Pinia

**Decision**: Use Pinia for Vue 3 state management
**Why**: Official Vue 3 recommendation, simpler than Vuex, TypeScript-first
**Alternatives**: Vuex (legacy), plain composables (less structured)

### Migrations: Alembic

**Decision**: Use Alembic for database migrations
**Why**: Standard Python migration tool, works well with asyncpg
**Alternatives**: Manual SQL scripts (less maintainable)

### Image Storage: AWS S3 with boto3

**Decision**: Use boto3 for S3 uploads
**Why**: Standard AWS SDK, well-documented, production-ready
**Alternatives**: MinIO (self-hosted S3-compatible), local storage (not scalable)

## Project Structure

```
xinyutian/
├── CLAUDE.md
├── Makefile
├── docker-compose.yml
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── alembic.ini
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   └── database.py
│   ├── migrations/
│   │   ├── env.py
│   │   └── versions/
│   └── scripts/
│       └── init_db.py
└── frontend/
    ├── Dockerfile
    ├── nginx.conf
    ├── package.json
    ├── vite.config.ts
    ├── tsconfig.json
    ├── index.html
    └── src/
        ├── main.ts
        ├── App.vue
        ├── router/
        │   └── index.ts
        └── stores/
```

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| Breaking existing functionality | Complete replacement, no migration path needed (demo project) |
| asyncpg complexity | Use connection pool pattern, keep queries simple |
| Vue 3 learning curve | Composition API is simpler than Options API |

## Migration Plan

1. Create new directory structure
2. Set up Docker Compose with PostgreSQL
3. Create basic FastAPI app with database connection
4. Create Vue 3 + Vite frontend scaffold
5. Create Makefile
6. Verify all services start correctly

No data migration needed (demo project with JSON files).

## Open Questions

- S3 bucket naming convention? (Use environment variables)
- JWT secret management? (Environment variables for now)

