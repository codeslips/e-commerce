"""Seed database with demo data."""
import asyncio
import json
import sys
from pathlib import Path
from decimal import Decimal
from datetime import datetime, timezone

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import db
from app.services.auth import hash_password


def get_seed_path():
    """Get the seed data folder path.
    
    In Docker: mounted at /seed
    Local development: relative path from backend/scripts to project root/seed
    """
    docker_path = Path("/seed")
    if docker_path.exists():
        return docker_path
    return Path(__file__).parent.parent.parent / "seed"


async def seed_users():
    """Load admin users from JSON file."""
    users_file = get_seed_path() / "users.json"
    
    if not users_file.exists():
        print(f"Users file not found: {users_file}")
        return []
    
    with open(users_file) as f:
        users_data = json.load(f)
    
    user_ids = []
    for user in users_data:
        existing = await db.fetchrow(
            "SELECT id FROM users WHERE username = $1",
            user["username"]
        )
        
        if existing:
            print(f"User '{user['username']}' already exists, skipping...")
            user_ids.append(existing["id"])
            continue
        
        result = await db.fetchrow(
            """
            INSERT INTO users (username, email, password_hash, role, is_active)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING id
            """,
            user["username"],
            user["email"],
            hash_password(user["password"]),
            user.get("role", "admin"),
            True
        )
        
        user_ids.append(result["id"])
        print(f"Created user: {user['username']} / {user['password']} ({user.get('role', 'admin')})")
    
    return user_ids


async def seed_products():
    """Load products from JSON file."""
    products_file = get_seed_path() / "products.json"
    
    if not products_file.exists():
        print(f"Products file not found: {products_file}")
        return []
    
    with open(products_file) as f:
        products_data = json.load(f)
    
    product_ids = []
    for product in products_data:
        # Check if product already exists
        existing = await db.fetchrow(
            "SELECT id FROM products WHERE name = $1",
            product["name"]
        )
        
        if existing:
            print(f"Product '{product['name']}' already exists, skipping...")
            product_ids.append(existing["id"])
            continue
        
        result = await db.fetchrow(
            """
            INSERT INTO products (name, category, price, unit, min_order_quantity, description, stock, is_active)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            RETURNING id
            """,
            product["name"],
            product["category"],
            Decimal(str(product["price"])),
            product["unit"],
            product["min_order_quantity"],
            product.get("description"),
            product["stock"],
            product.get("is_active", True)
        )
        product_ids.append(result["id"])
        print(f"Created product: {product['name']}")
    
    return product_ids


async def seed_dealers():
    """Load dealers from JSON file."""
    dealers_file = get_seed_path() / "dealers.json"
    
    if not dealers_file.exists():
        print(f"Dealers file not found: {dealers_file}")
        return {}
    
    with open(dealers_file) as f:
        dealers_data = json.load(f)
    
    dealer_map = {}  # username -> dealer_id
    for dealer in dealers_data:
        # Check if user already exists
        existing = await db.fetchrow(
            "SELECT id FROM users WHERE username = $1",
            dealer["username"]
        )
        
        if existing:
            print(f"Dealer '{dealer['username']}' already exists, skipping...")
            # Get dealer ID
            dealer_record = await db.fetchrow(
                "SELECT id FROM dealers WHERE user_id = $1",
                existing["id"]
            )
            if dealer_record:
                dealer_map[dealer["username"]] = dealer_record["id"]
            continue
        
        # Create user
        user = await db.fetchrow(
            """
            INSERT INTO users (username, email, password_hash, role, is_active)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING id
            """,
            dealer["username"],
            dealer["email"],
            hash_password(dealer["password"]),
            "dealer",
            True
        )
        
        # Create dealer
        dealer_record = await db.fetchrow(
            """
            INSERT INTO dealers (user_id, company_name, contact_name, phone, address, status)
            VALUES ($1, $2, $3, $4, $5, $6)
            RETURNING id
            """,
            user["id"],
            dealer["company_name"],
            dealer["contact_name"],
            dealer["phone"],
            dealer.get("address"),
            dealer.get("status", "pending")
        )
        
        dealer_map[dealer["username"]] = dealer_record["id"]
        print(f"Created dealer: {dealer['company_name']} ({dealer['username']} / {dealer['password']}) - {dealer.get('status', 'pending')}")
    
    return dealer_map


async def seed_orders(dealer_map):
    """Load orders from JSON file."""
    orders_file = get_seed_path() / "orders.json"
    
    if not orders_file.exists():
        print(f"Orders file not found: {orders_file}")
        return
    
    # Check if orders already exist
    existing_count = await db.fetchval("SELECT COUNT(*) FROM orders")
    if existing_count > 0:
        print(f"Orders already exist ({existing_count}), skipping...")
        return
    
    with open(orders_file) as f:
        orders_data = json.load(f)
    
    # Get all products for lookup
    products = await db.fetch("SELECT id, name, price FROM products")
    product_map = {p["name"]: {"id": p["id"], "price": p["price"]} for p in products}
    
    for i, order in enumerate(orders_data):
        dealer_username = order["dealer_username"]
        dealer_id = dealer_map.get(dealer_username)
        
        if not dealer_id:
            print(f"Dealer '{dealer_username}' not found, skipping order...")
            continue
        
        # Calculate total from items
        total = Decimal("0")
        order_items = []
        for item in order["items"]:
            product_info = product_map.get(item["product_name"])
            if not product_info:
                print(f"Product '{item['product_name']}' not found, skipping item...")
                continue
            
            quantity = item["quantity"]
            unit_price = product_info["price"]
            subtotal = unit_price * quantity
            total += subtotal
            
            order_items.append({
                "product_id": product_info["id"],
                "product_name": item["product_name"],
                "quantity": quantity,
                "unit_price": unit_price,
                "subtotal": subtotal
            })
        
        if not order_items:
            print(f"No valid items for order, skipping...")
            continue
        
        order_no = f"ORD{datetime.now(timezone.utc).strftime('%Y%m%d')}{(i + 1):03d}"
        
        order_record = await db.fetchrow(
            """
            INSERT INTO orders (order_no, dealer_id, status, total_amount, shipping_address, notes)
            VALUES ($1, $2, $3, $4, $5, $6)
            RETURNING id
            """,
            order_no,
            dealer_id,
            order["status"],
            total,
            order["shipping_address"],
            order.get("notes", "")
        )
        
        # Add order items
        for item in order_items:
            await db.execute(
                """
                INSERT INTO order_items (order_id, product_id, product_name, quantity, unit_price, subtotal)
                VALUES ($1, $2, $3, $4, $5, $6)
                """,
                order_record["id"],
                item["product_id"],
                item["product_name"],
                item["quantity"],
                item["unit_price"],
                item["subtotal"]
            )
        
        print(f"Created order: {order_no} ({order['status']}) - {len(order_items)} items, ¥{total:.2f}")


async def main():
    """Run all seed operations."""
    print("Connecting to database...")
    await db.connect()
    
    try:
        print("\n=== Seeding Admin Users ===")
        await seed_users()
        
        print("\n=== Seeding Products ===")
        await seed_products()
        
        print("\n=== Seeding Dealers ===")
        dealer_map = await seed_dealers()
        
        print("\n=== Seeding Orders ===")
        await seed_orders(dealer_map)
        
        print("\n=== Seed Complete ===")
        print("\nDemo Accounts:")
        print("  Admin: admin / admin123")
        print("  Dealer: dealer001 / dealer123 (approved)")
        print("  Dealer: dealer002 / dealer123 (approved)")
        print("  Dealer: dealer003 / dealer123 (approved)")
        print("  Dealer: dealer004 / dealer123 (pending)")
        print("  Dealer: dealer005 / dealer123 (suspended)")
        
    finally:
        await db.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
