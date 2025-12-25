# Change: Add Complete Business Logic and Seed Data

## Why

The basic project scaffold is complete (Phase 1). Phase 2 implements the full business logic for the B2B dealer ordering platform, including authentication, product management, order processing, dealer management, and seed data for demonstration.

## What Changes

### Backend
- Add JWT-based authentication system (login, logout, token refresh)
- Add product CRUD operations with category management
- Add order creation, listing, and status management
- Add dealer CRUD and approval workflow
- Add file storage service with local storage backend (S3-compatible API for future migration)
- Add Pydantic schemas for all entities
- Add API routers for auth, products, orders, dealers
- Add seed data script with demo products, dealers, and orders

### Frontend
- Add authentication (login page, auth state, protected routes)
- Add product catalog with filtering and search
- Add shopping cart with persistence
- Add order creation and history views
- Add admin dashboard with CRUD operations
- Add API client with authentication interceptors

### Infrastructure
- Mount `/data/images` volume for local image storage
- Add `make seed` command for data initialization

## Image Storage Strategy

Use local file storage (`/data/images`) initially with an abstraction layer that mirrors S3 API:
- `storage.save(file, path)` → saves file to local path
- `storage.get_url(path)` → returns accessible URL
- `storage.delete(path)` → removes file

Configuration via `STORAGE_BACKEND=local|s3` environment variable allows seamless migration to S3 later.

## Impact

- Affected specs: `project-bootstrap` (MODIFIED - remove stub requirement)
- New specs: `user-auth`, `product-management`, `order-management`, `dealer-management`, `file-storage`, `seed-data`
- Affected code: `backend/app/`, `frontend/src/`, `docker-compose.yml`, `Makefile`

## Out of Scope

- Password reset flow
- Email notifications
- Inventory tracking (real-time stock deduction)
- Payment integration
- Logging and monitoring

