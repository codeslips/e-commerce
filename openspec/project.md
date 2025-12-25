# Project Context

## Purpose

欣与甜订货平台 (Xin Yu Tian Dealer Ordering Platform) - A B2B dealer ordering platform for a food production company. The platform enables dealers to browse products, place orders, and manage their order history. Internal staff can manage products, orders, dealers, and inventory through an admin panel.

## Tech Stack

- **Frontend**: Vue 3 + Vite + TypeScript
- **Backend**: FastAPI + asyncpg (async PostgreSQL)
- **Database**: PostgreSQL (single instance)
- **Image Storage**: AWS S3 (via boto3)
- **Containerization**: Docker + Docker Compose

## Project Conventions

### Code Style

- **Python (Backend)**:
  - Use Pydantic models for data validation
  - Follow FastAPI conventions for route definitions
  - Use type hints for all function parameters and return values
  - Keep API responses in JSON format
  - Use asyncpg for async database operations

- **TypeScript (Frontend)**:
  - Vue 3 Composition API with `<script setup>`
  - Pinia for state management
  - Vue Router for navigation
  - TypeScript strict mode enabled

- **Naming**:
  - Files: kebab-case for Vue components, snake_case for Python
  - Python: snake_case for functions/variables, PascalCase for classes
  - TypeScript: camelCase for functions/variables, PascalCase for types/classes

### Architecture Patterns

- **Separation of Concerns**: Frontend and backend are independent services
- **RESTful API**: Backend exposes REST endpoints under `/api/` prefix
- **PostgreSQL Database**: Single database instance with asyncpg connection pool
- **S3 Image Storage**: Product images stored in AWS S3
- **CORS Enabled**: For local development cross-origin requests

### API Structure

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check with database status |
| GET | `/api/products` | List products (with pagination) |
| GET | `/api/products/{id}` | Get product detail |
| POST | `/api/products` | Create product (admin) |
| PUT | `/api/products/{id}` | Update product (admin) |
| DELETE | `/api/products/{id}` | Delete product (admin) |
| GET | `/api/orders` | List orders |
| GET | `/api/orders/{id}` | Get order detail |
| POST | `/api/orders` | Create order (dealer) |
| PUT | `/api/orders/{id}/status` | Update order status (admin) |
| GET | `/api/dealers` | List dealers (admin) |
| POST | `/api/auth/login` | User login |
| POST | `/api/auth/logout` | User logout |

### Testing Strategy

- Manual testing via browser and API documentation (`/docs`)
- Backend health check endpoint for container monitoring

### Git Workflow

- Feature branches for new capabilities
- Direct commits to main for minor fixes
- Commit messages in English, descriptive of changes

## Domain Context

### Users & Authentication
- Two roles: `admin` and `dealer`
- JWT-based authentication
- Dealers must be approved before placing orders

### Products
- Products belong to categories (烘焙食品, 零食, etc.)
- Each product has ID, name, category, price, unit, description, image_url, stock
- Images stored in S3

### Orders
- Order numbers format: `ORD20240101001`
- Status: pending, confirmed, shipped, delivered, cancelled
- Orders contain multiple order items with product snapshots

### Dealers
- Company information: name, contact, phone, address
- Status: pending, approved, suspended

## Important Constraints

- **Single PostgreSQL Database**: All data stored in one database instance
- **S3 for Images**: Product images uploaded to AWS S3
- **No Logging/Monitoring**: Not included per requirements
- **Chinese Language**: UI primarily in Simplified Chinese with English labels

## External Dependencies

### Backend (Python)
- fastapi, uvicorn
- asyncpg (async PostgreSQL)
- alembic (database migrations)
- pydantic, pydantic-settings
- boto3 (AWS S3)
- python-jose, passlib (authentication)

### Frontend
- Vue 3, Vue Router, Pinia
- Vite, TypeScript
- Axios

### Infrastructure
- Docker & Docker Compose
- Nginx (frontend container)
- PostgreSQL 16

### Ports
- Frontend: `5500` (external) → `80` (container)
- Backend API: `9111` (external) → `9111` (container)
- PostgreSQL: `5432`
- API Docs: `http://localhost:9111/docs`

## Makefile Commands

```bash
make up          # Start all services (production mode)
make dev         # Start development mode (with logs)
make stop        # Stop all services
make db-init     # Initialize database (create tables)
make db-migrate  # Run database migrations
make logs        # View logs
make clean       # Clean up everything including volumes
```
