import json
import os
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models import Order, Product, SearchQuery

app = FastAPI(title="欣与甜 E-Shop API", version="1.0.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_PATH = os.environ.get("DATA_PATH", "./data")


def load_orders() -> List[dict]:
    try:
        with open(os.path.join(DATA_PATH, "orders.json"), "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def load_products() -> List[dict]:
    try:
        with open(os.path.join(DATA_PATH, "products.json"), "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/api/orders", response_model=List[Order])
def get_orders():
    return load_orders()


@app.get("/api/orders/{order_id}", response_model=Order)
def get_order(order_id: str):
    orders = load_orders()
    for order in orders:
        if order.get("order_id") == order_id:
            return order
    raise HTTPException(status_code=404, detail="Order not found")


@app.post("/api/orders/search", response_model=List[Order])
def search_orders(query: SearchQuery):
    orders = load_orders()
    query_str = query.query_str.lower()
    results = []
    for order in orders:
        if (
            query_str in order.get("order_id", "").lower()
            or query_str in order.get("tracking_number", "").lower()
            or query_str in order.get("recipient_name", "").lower()
            or query_str in order.get("recipient_phone", "").lower()
        ):
            results.append(order)
    return results


@app.get("/api/products", response_model=List[Product])
def get_products():
    return load_products()


@app.get("/api/products/{product_id}", response_model=Product)
def get_product(product_id: str):
    products = load_products()
    for product in products:
        if product.get("product_id") == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")

