from pydantic import BaseModel
from typing import List, Optional


class TrackingEvent(BaseModel):
    time: str
    location: str
    status: str


class Order(BaseModel):
    order_id: str
    tracking_number: str
    recipient_name: str
    recipient_phone: str
    product_name: str
    status: str
    courier: str
    shipping_date: str
    estimated_delivery: str
    tracking_history: List[TrackingEvent] = []


class Product(BaseModel):
    product_id: str
    name: str
    category: str
    price: float
    description: str
    image: str
    in_stock: bool


class SearchQuery(BaseModel):
    query_str: str

