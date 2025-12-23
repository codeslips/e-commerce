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

# 欣与甜 E-Shop Demo Project

## Project Overview

A self-service order tracking and e-shop website inspired by "欣与甜" (Xin Yu Tian) food shop. Customers can query their delivery/order status by entering order number, recipient name, or phone number.

## Tech Stack

- **Frontend**: Vanilla JavaScript + Tailwind CSS
- **Backend**: FastAPI (Python)
- **Data Storage**: Local JSON files (no database required)

## Project Structure

```
xinyutian/
├── CLAUDE.md                 # Project documentation
├── data/
│   ├── orders.json           # Demo order data
│   ├── products.json         # Demo product data
│   └── reference/            # Reference files
│       └── 欣与甜订单自助快递查询官网.html
├── backend/
│   ├── main.py               # FastAPI application entry
│   ├── requirements.txt      # Python dependencies
│   └── models.py             # Pydantic models
└── frontend/
    ├── index.html            # Main page
    ├── css/
    │   └── style.css         # Custom styles (if needed)
    └── js/
        └── app.js            # Main JavaScript logic
```

## Features

1. **Order Query System**
   - Search by order/tracking number
   - Search by recipient name
   - Search by phone number
   - Search history (localStorage)

2. **Product Categories**
   - Display product category buttons
   - Link to product pages

3. **Responsive Design**
   - Mobile-first approach
   - Works on desktop and mobile devices

## API Endpoints

### Orders

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/orders` | Get all orders |
| GET | `/api/orders/{order_id}` | Get single order by ID |
| POST | `/api/orders/search` | Search orders by query string |

### Products

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/products` | Get all products |
| GET | `/api/products/{product_id}` | Get single product |

## Data Models

### Order
```json
{
  "order_id": "YT20231223001",
  "tracking_number": "SF1234567890",
  "recipient_name": "张三",
  "recipient_phone": "13800138000",
  "product_name": "蛋皮吐司",
  "status": "已发货",
  "courier": "顺丰速运",
  "shipping_date": "2023-12-20",
  "estimated_delivery": "2023-12-25",
  "tracking_history": [
    {
      "time": "2023-12-20 10:00",
      "location": "广州市",
      "status": "已揽收"
    }
  ]
}
```

### Product
```json
{
  "product_id": "p001",
  "name": "蛋皮吐司",
  "category": "烘焙食品",
  "price": 29.90,
  "description": "新鲜烘焙蛋皮吐司",
  "image": "https://example.com/image.jpg",
  "in_stock": true
}
```

## Setup Instructions

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend

Simply open `frontend/index.html` in a browser, or serve it:

```bash
cd frontend
python -m http.server 5500
```

Or configure FastAPI to serve static files (recommended for production).

## Docker Setup

### Project Structure with Docker

```
xinyutian/
├── docker-compose.yml        # Docker Compose configuration
├── backend/
│   ├── Dockerfile            # Backend container config
│   └── ...
└── frontend/
    ├── Dockerfile            # Frontend container config (nginx)
    └── ...
```

### Quick Start with Docker

```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d --build

# Stop all services
docker-compose down
```

### Access Points

- **Frontend**: http://localhost:5500
- **Backend API**: http://localhost:9111
- **API Docs**: http://localhost:9111/docs

## Development Notes

- CORS is enabled for local development
- All API responses return JSON
- Search is case-insensitive and supports partial matching
- Frontend uses Tailwind CSS via CDN for styling

