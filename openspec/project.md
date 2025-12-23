# Project Context

## Purpose

欣与甜 (Xin Yu Tian) E-Shop Demo - A self-service order tracking and e-shop website for a food shop. Customers can query their delivery/order status by entering order number, recipient name, or phone number. The project also displays product categories with links to product pages.

## Tech Stack

- **Frontend**: Vanilla JavaScript + Tailwind CSS (via CDN)
- **Backend**: FastAPI (Python)
- **Data Storage**: Local JSON files (`data/orders.json`, `data/products.json`)
- **Containerization**: Docker + Docker Compose
- **Web Server**: Nginx (for frontend container)

## Project Conventions

### Code Style

- **Python (Backend)**:
  - Use Pydantic models for data validation
  - Follow FastAPI conventions for route definitions
  - Use type hints for all function parameters and return values
  - Keep API responses in JSON format

- **JavaScript (Frontend)**:
  - Vanilla JS (no frameworks)
  - Use `localStorage` for search history persistence
  - DOM manipulation with standard APIs

- **CSS**:
  - Tailwind CSS via CDN for styling
  - Custom styles in `frontend/css/style.css` only when necessary
  - Mobile-first responsive design

- **Naming**:
  - Files: kebab-case (`main.py`, `app.js`, `style.css`)
  - Python: snake_case for functions/variables, PascalCase for classes
  - JavaScript: camelCase for functions/variables

### Architecture Patterns

- **Separation of Concerns**: Frontend and backend are independent services
- **RESTful API**: Backend exposes REST endpoints under `/api/` prefix
- **Static Data**: JSON files as data source (no database)
- **CORS Enabled**: For local development cross-origin requests

### API Structure

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/orders` | Get all orders |
| GET | `/api/orders/{order_id}` | Get single order by ID |
| POST | `/api/orders/search` | Search orders by query string |
| GET | `/api/products` | Get all products |
| GET | `/api/products/{product_id}` | Get single product |

### Testing Strategy

- Manual testing via browser and API documentation (`/docs`)
- No automated test suite currently (demo project)

### Git Workflow

- Feature branches for new capabilities
- Direct commits to main for minor fixes
- Commit messages in English, descriptive of changes

## Domain Context

### Order Tracking
- Orders have unique IDs (format: `YT20231223001`)
- Each order includes tracking number, recipient info, courier details
- Tracking history shows package journey with timestamps and locations
- Status values: 待发货, 已发货, 运输中, 已签收 (Pending, Shipped, In Transit, Delivered)

### Products
- Products belong to categories (烘焙食品, 零食, etc.)
- Each product has ID, name, category, price, description, image, stock status

### Couriers
- Supported: 顺丰速运, 中通快递, 圆通速递, 韵达快递

### Search Behavior
- Case-insensitive matching
- Supports partial matching
- Can search by: order_id, tracking_number, recipient_name, recipient_phone

## Important Constraints

- **No Database**: Data stored in JSON files only - suitable for demo/small scale
- **Read-Only Data**: Backend mounts data volume as read-only (`ro`)
- **Demo Purpose**: Not designed for production use with real transactions
- **Chinese Language**: UI and data primarily in Simplified Chinese

## External Dependencies

### Backend (Python)
- fastapi
- uvicorn
- pydantic

### Frontend
- Tailwind CSS (CDN: https://cdn.tailwindcss.com)

### Infrastructure
- Docker & Docker Compose
- Nginx (frontend container)

### Ports
- Frontend: `5500` (external) → `80` (container)
- Backend API: `9000` (external) → `8000` (container)
- API Docs: `http://localhost:9000/docs`
