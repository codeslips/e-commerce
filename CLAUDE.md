<!-- OPENSPEC:START -->
# OpenSpec Instructions

These instructions are for AI assistants working in this project.

Always open `@/openspec/AGENTS.md` when the request:
- Mentions planning or proposals (words like proposal, spec, change, plan)
- Introduces new capabilities, breaking changes, architecture shifts, or big performance/security work
- Sounds ambiguous and you need the authoritative spec before coding

Use `@/openspec/AGENTS.md` to learn:
- How to create and apply change proposals
- Spec format and conventions
- Project structure and guidelines

Keep this managed block so 'openspec update' can refresh the instructions.

<!-- OPENSPEC:END -->

# 欣与甜订货平台 (Xin Yu Tian Dealer Ordering Platform)

## Project Overview

A B2B dealer ordering platform for a food production company. The platform enables dealers to browse products, place orders, and manage their order history. Internal staff can manage products, orders, dealers, and inventory through an admin panel.

## Tech Stack

- **Frontend**: Vue 3 + Vite + TypeScript
- **Backend**: FastAPI + asyncpg (async PostgreSQL)
- **Database**: PostgreSQL (single instance)
- **Image Storage**: AWS S3 (via boto3)
- **Containerization**: Docker + Docker Compose

## Project Structure

```
xinyutian/
├── CLAUDE.md                 # Project documentation
├── Makefile                  # Common commands (up, dev, stop, db-init, db-migrate)
├── docker-compose.yml        # Docker Compose configuration
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app/
│   │   ├── main.py           # FastAPI application entry
│   │   ├── config.py         # Configuration settings
│   │   ├── database.py       # Database connection (asyncpg)
│   │   ├── models/           # SQLAlchemy/Pydantic models
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── product.py
│   │   │   ├── order.py
│   │   │   └── dealer.py
│   │   ├── routers/          # API route handlers
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── products.py
│   │   │   ├── orders.py
│   │   │   ├── dealers.py
│   │   │   └── admin.py
│   │   ├── services/         # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── s3.py         # S3 image upload service
│   │   │   ├── auth.py
│   │   │   └── order.py
│   │   └── schemas/          # Pydantic schemas
│   │       ├── __init__.py
│   │       ├── user.py
│   │       ├── product.py
│   │       ├── order.py
│   │       └── dealer.py
│   ├── migrations/           # Database migrations
│   │   ├── versions/
│   │   └── env.py
│   └── scripts/
│       ├── init_db.py        # Database initialization
│       └── seed_data.py      # Demo data seeding
├── frontend/
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── index.html
│   └── src/
│       ├── main.ts
│       ├── App.vue
│       ├── router/           # Vue Router
│       │   └── index.ts
│       ├── stores/           # Pinia stores
│       │   ├── auth.ts
│       │   ├── cart.ts
│       │   └── product.ts
│       ├── api/              # API client
│       │   └── index.ts
│       ├── components/       # Shared components
│       ├── views/
│       │   ├── dealer/       # Dealer portal views
│       │   │   ├── Home.vue
│       │   │   ├── Products.vue
│       │   │   ├── Cart.vue
│       │   │   ├── Orders.vue
│       │   │   └── Profile.vue
│       │   └── admin/        # Admin panel views
│       │       ├── Dashboard.vue
│       │       ├── Products.vue
│       │       ├── Orders.vue
│       │       ├── Dealers.vue
│       │       └── Settings.vue
│       └── assets/
└── data/
    └── seed/                 # Seed data for initialization
        ├── products.json
        └── dealers.json
```

## Features

### Dealer Portal (经销商端)

1. **Authentication**
   - Dealer login/logout
   - Password reset
   - Profile management

2. **Product Browsing**
   - View product catalog by category
   - Product search and filtering
   - Product detail view with images

3. **Shopping Cart**
   - Add/remove products
   - Update quantities
   - Cart persistence

4. **Order Management**
   - Place orders from cart
   - View order history
   - Order status tracking
   - Order detail view

### Admin Panel (管理后台)

1. **Dashboard**
   - Order statistics overview
   - Recent orders
   - Low stock alerts

2. **Product Management**
   - CRUD operations for products
   - Category management
   - Image upload to S3
   - Inventory management

3. **Order Management**
   - View all orders
   - Update order status
   - Order filtering and search

4. **Dealer Management**
   - CRUD operations for dealers
   - Dealer approval/suspension
   - View dealer order history

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/login` | User login |
| POST | `/api/auth/logout` | User logout |
| POST | `/api/auth/refresh` | Refresh token |
| GET | `/api/auth/me` | Get current user |

### Products

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/products` | List products (with pagination) |
| GET | `/api/products/{id}` | Get product detail |
| POST | `/api/products` | Create product (admin) |
| PUT | `/api/products/{id}` | Update product (admin) |
| DELETE | `/api/products/{id}` | Delete product (admin) |
| GET | `/api/products/categories` | List categories |
| POST | `/api/products/{id}/image` | Upload product image to S3 |

### Orders

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/orders` | List orders (filtered by role) |
| GET | `/api/orders/{id}` | Get order detail |
| POST | `/api/orders` | Create order (dealer) |
| PUT | `/api/orders/{id}/status` | Update order status (admin) |
| DELETE | `/api/orders/{id}` | Cancel order |

### Dealers

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/dealers` | List dealers (admin) |
| GET | `/api/dealers/{id}` | Get dealer detail |
| POST | `/api/dealers` | Create dealer (admin) |
| PUT | `/api/dealers/{id}` | Update dealer (admin) |
| PUT | `/api/dealers/{id}/status` | Update dealer status (admin) |

## Data Models

### User
```json
{
  "id": "uuid",
  "username": "dealer001",
  "email": "dealer@example.com",
  "password_hash": "...",
  "role": "dealer|admin",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### Dealer
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "company_name": "某某食品店",
  "contact_name": "张三",
  "phone": "13800138000",
  "address": "广州市天河区...",
  "status": "pending|approved|suspended",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Product
```json
{
  "id": "uuid",
  "name": "蛋皮吐司",
  "category": "烘焙食品",
  "price": 29.90,
  "unit": "袋",
  "min_order_quantity": 10,
  "description": "新鲜烘焙蛋皮吐司",
  "image_url": "https://s3.amazonaws.com/bucket/products/xxx.jpg",
  "stock": 1000,
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### Order
```json
{
  "id": "uuid",
  "order_no": "ORD20240101001",
  "dealer_id": "uuid",
  "status": "pending|confirmed|shipped|delivered|cancelled",
  "total_amount": 2990.00,
  "shipping_address": "广州市天河区...",
  "notes": "请尽快发货",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z",
  "items": [
    {
      "id": "uuid",
      "product_id": "uuid",
      "product_name": "蛋皮吐司",
      "quantity": 100,
      "unit_price": 29.90,
      "subtotal": 2990.00
    }
  ]
}
```

## Environment Variables

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/xinyutian

# JWT
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60

# AWS S3
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_S3_BUCKET=xinyutian-images
AWS_S3_REGION=ap-southeast-1

# App
APP_ENV=development
CORS_ORIGINS=http://localhost:5173,http://localhost:5500
```

## Makefile Commands

```bash
# Start all services (production mode)
make up

# Start development mode (with hot reload)
make dev

# Stop all services
make stop

# Initialize database (create tables)
make db-init

# Run database migrations
make db-migrate
```

## Docker Setup

### Quick Start

```bash
# Build and start all services
make up

# Or using docker-compose directly
docker-compose up --build -d
```

### Access Points

- **Frontend (Dealer Portal)**: http://localhost:5500
- **Frontend (Admin Panel)**: http://localhost:5500/admin
- **Backend API**: http://localhost:9111
- **API Docs**: http://localhost:9111/docs
- **PostgreSQL**: localhost:5432

## Development Notes

- CORS is enabled for local development
- All API responses return JSON
- Authentication uses JWT tokens
- Images are stored in AWS S3
- Database uses asyncpg for async operations
- Frontend uses Vue 3 Composition API with TypeScript
