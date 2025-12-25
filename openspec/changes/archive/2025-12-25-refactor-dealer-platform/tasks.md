## 1. Backend Infrastructure

- [x] 1.1 Create backend directory structure (`app/`, `migrations/`, `scripts/`)
- [x] 1.2 Create `app/config.py` with environment variable handling
- [x] 1.3 Create `app/database.py` with asyncpg connection pool
- [x] 1.4 Create `app/main.py` with FastAPI app and health endpoint
- [x] 1.5 Update `requirements.txt` with new dependencies (asyncpg, boto3, alembic, pydantic-settings)
- [x] 1.6 Create `alembic.ini` and `migrations/env.py` for database migrations
- [x] 1.7 Create initial migration with base schema (users table placeholder)
- [x] 1.8 Create `scripts/init_db.py` for database initialization
- [x] 1.9 Update backend `Dockerfile` for new structure

## 2. Frontend Infrastructure

- [x] 2.1 Remove old Vanilla JS files
- [x] 2.2 Create Vue 3 + Vite project structure
- [x] 2.3 Create `package.json` with dependencies (vue, vite, vue-router, pinia, typescript)
- [x] 2.4 Create `vite.config.ts` with API proxy configuration
- [x] 2.5 Create `tsconfig.json`
- [x] 2.6 Create `src/main.ts` entry point
- [x] 2.7 Create `src/App.vue` root component
- [x] 2.8 Create `src/router/index.ts` with basic routes
- [x] 2.9 Update frontend `Dockerfile` for Vite build
- [x] 2.10 Update `nginx.conf` for Vue SPA routing

## 3. Docker & Infrastructure

- [x] 3.1 Update `docker-compose.yml` with PostgreSQL service
- [x] 3.2 Add environment variables for database, S3, JWT
- [x] 3.3 Create `Makefile` with up, dev, stop, db-init, db-migrate commands

## 4. Verification

- [ ] 4.1 Run `make up` and verify all containers start
- [ ] 4.2 Verify backend health endpoint responds
- [ ] 4.3 Verify frontend loads in browser
- [ ] 4.4 Verify database connection works

**Note**: Verification tasks require Docker access. Run `make up` to test the deployment.
