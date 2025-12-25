## Context

Phase 2 implementation of business logic for the B2B dealer ordering platform. This involves authentication, CRUD operations for products/orders/dealers, and a file storage abstraction layer.

## Goals / Non-Goals

### Goals
- Complete authentication flow (login, logout, token refresh)
- Product CRUD with image upload
- Order workflow (create, list, status updates)
- Dealer management with approval workflow
- Seed data for demonstration
- File storage abstraction (local first, S3-ready)

### Non-Goals
- Password reset / email verification
- Real-time inventory deduction
- Payment processing
- Logging infrastructure

## Architecture Decisions

### File Storage Abstraction

**Decision**: Create `StorageService` interface with `LocalStorage` and `S3Storage` implementations

```python
class StorageService(ABC):
    @abstractmethod
    async def save(self, file: UploadFile, path: str) -> str: ...
    
    @abstractmethod
    def get_url(self, path: str) -> str: ...
    
    @abstractmethod
    async def delete(self, path: str) -> bool: ...

class LocalStorage(StorageService):
    """Saves to /data/images, returns /api/files/{path}"""

class S3Storage(StorageService):
    """Saves to S3 bucket, returns S3 URL"""
```

**Configuration**: `STORAGE_BACKEND=local|s3` environment variable

**Local Storage URL Pattern**: `/api/files/{path}` served by FastAPI static files

### Authentication Flow

**Decision**: JWT with access + refresh tokens

- Access token: 60 minutes expiry, stored in memory/localStorage
- Refresh token: 7 days expiry, stored in httpOnly cookie
- Token refresh via `/api/auth/refresh`

### Order Number Generation

**Decision**: Sequential format `ORD{YYYYMMDD}{NNN}`

- Date-based prefix for easy identification
- Daily sequence counter stored in database
- Example: `ORD20241225001`, `ORD20241225002`

### Role-Based Access Control

**Decision**: Simple role check via JWT claims

- `admin`: Full access to all endpoints
- `dealer`: Access to products (read), orders (CRUD own), profile

Implemented as FastAPI dependencies:
- `get_current_user`: Extracts user from JWT
- `require_admin`: Raises 403 if not admin
- `require_approved_dealer`: Checks dealer status

## Database Schema (existing from migration 001)

```
users: id, username, email, password_hash, role, is_active, created_at, updated_at
dealers: id, user_id, company_name, contact_name, phone, address, status, created_at
products: id, name, category, price, unit, min_order_quantity, description, image_url, stock, is_active, created_at, updated_at
orders: id, order_no, dealer_id, status, total_amount, shipping_address, notes, created_at, updated_at
order_items: id, order_id, product_id, product_name, quantity, unit_price, subtotal
```

## Seed Data Structure

### Demo Admin User
- Username: `admin`
- Password: `admin123`
- Role: `admin`

### Demo Dealers (3)
| Company | Contact | Status |
|---------|---------|--------|
| 广州好味道食品店 | 张三 | approved |
| 深圳鲜食坊 | 李四 | approved |
| 佛山美味轩 | 王五 | pending |

### Demo Products (8)
| Name | Category | Price | Stock |
|------|----------|-------|-------|
| 蛋皮吐司 | 烘焙食品 | 29.90 | 1000 |
| 肉松面包 | 烘焙食品 | 25.00 | 800 |
| 奶香小馒头 | 烘焙食品 | 18.00 | 1500 |
| 葱油饼 | 烘焙食品 | 22.00 | 600 |
| 牛肉干 | 零食 | 58.00 | 500 |
| 鱼豆腐 | 零食 | 35.00 | 800 |
| 海苔卷 | 零食 | 28.00 | 1200 |
| 芝麻糖 | 零食 | 15.00 | 2000 |

### Demo Orders (5)
- Mix of pending, confirmed, shipped, delivered statuses
- Associated with approved dealers

## API Response Patterns

### Pagination
```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "page_size": 20,
  "pages": 5
}
```

### Error Response
```json
{
  "detail": "Error message"
}
```

## Frontend State Management

### Pinia Stores
- `auth.ts`: User state, login/logout actions, token management
- `cart.ts`: Cart items, add/remove/update actions, localStorage persistence
- `product.ts`: Products cache, filtering state

### Protected Routes
- `/admin/*`: Requires admin role
- `/orders`, `/cart`, `/profile`: Requires authenticated dealer

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| JWT token in localStorage vulnerable to XSS | Use httpOnly cookie for refresh token |
| Local file storage not scalable | Abstraction layer enables S3 migration |
| No email verification | Manual dealer approval by admin |

## Migration Plan

1. Implement backend services (auth, products, orders, dealers, storage)
2. Implement backend routers
3. Implement seed data script
4. Implement frontend stores and API client
5. Implement frontend views
6. Update docker-compose for /data/images volume
7. Add `make seed` command

