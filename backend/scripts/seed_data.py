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


async def seed_admin():
    """Create admin user if not exists."""
    existing = await db.fetchrow(
        "SELECT id FROM users WHERE username = $1",
        "admin"
    )
    
    if existing:
        print("Admin user already exists, skipping...")
        return existing["id"]
    
    admin = await db.fetchrow(
        """
        INSERT INTO users (username, email, password_hash, role, is_active)
        VALUES ($1, $2, $3, $4, $5)
        RETURNING id
        """,
        "admin",
        "admin@xinyutian.com",
        hash_password("admin123"),
        "admin",
        True
    )
    
    print("Created admin user: admin / admin123")
    return admin["id"]


async def seed_products():
    """Load products from JSON file."""
    products_file = Path(__file__).parent.parent.parent / "data" / "seed" / "products.json"
    
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
    dealers_file = Path(__file__).parent.parent.parent / "data" / "seed" / "dealers.json"
    
    if not dealers_file.exists():
        print(f"Dealers file not found: {dealers_file}")
        return []
    
    with open(dealers_file) as f:
        dealers_data = json.load(f)
    
    dealer_ids = []
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
                dealer_ids.append(dealer_record["id"])
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
        
        dealer_ids.append(dealer_record["id"])
        print(f"Created dealer: {dealer['company_name']} ({dealer['username']} / {dealer['password']})")
    
    return dealer_ids


async def seed_orders(dealer_ids, product_ids):
    """Create demo orders."""
    if not dealer_ids or not product_ids:
        print("No dealers or products to create orders, skipping...")
        return
    
    # Check if orders already exist
    existing_count = await db.fetchval("SELECT COUNT(*) FROM orders")
    if existing_count > 0:
        print(f"Orders already exist ({existing_count}), skipping...")
        return
    
    # Get products for order items
    products = await db.fetch(
        "SELECT id, name, price FROM products WHERE id = ANY($1::uuid[])",
        product_ids[:4]  # Use first 4 products
    )
    
    # Create orders for approved dealers
    approved_dealers = await db.fetch(
        "SELECT id FROM dealers WHERE status = 'approved' AND id = ANY($1::uuid[])",
        dealer_ids
    )
    
    statuses = ["pending", "confirmed", "shipped", "delivered", "pending"]
    
    for i, dealer in enumerate(approved_dealers):
        for j, status in enumerate(statuses[:3] if i == 0 else statuses[3:]):
            order_no = f"ORD{datetime.now(timezone.utc).strftime('%Y%m%d')}{(i * 3 + j + 1):03d}"
            
            # Calculate total from 2-3 random products
            order_products = products[:(j % 3 + 1)]
            total = sum(p["price"] * 10 for p in order_products)
            
            order = await db.fetchrow(
                """
                INSERT INTO orders (order_no, dealer_id, status, total_amount, shipping_address, notes)
                VALUES ($1, $2, $3, $4, $5, $6)
                RETURNING id
                """,
                order_no,
                dealer["id"],
                status,
                total,
                "广州市天河区天河路123号",
                f"测试订单 {j + 1}"
            )
            
            # Add order items
            for product in order_products:
                await db.execute(
                    """
                    INSERT INTO order_items (order_id, product_id, product_name, quantity, unit_price, subtotal)
                    VALUES ($1, $2, $3, $4, $5, $6)
                    """,
                    order["id"],
                    product["id"],
                    product["name"],
                    10,
                    product["price"],
                    product["price"] * 10
                )
            
            print(f"Created order: {order_no} ({status})")


async def main():
    """Run all seed operations."""
    print("Connecting to database...")
    await db.connect()
    
    try:
        print("\n=== Seeding Admin User ===")
        await seed_admin()
        
        print("\n=== Seeding Products ===")
        product_ids = await seed_products()
        
        print("\n=== Seeding Dealers ===")
        dealer_ids = await seed_dealers()
        
        print("\n=== Seeding Orders ===")
        await seed_orders(dealer_ids, product_ids)
        
        print("\n=== Seed Complete ===")
        print("\nDemo Accounts:")
        print("  Admin: admin / admin123")
        print("  Dealer: dealer001 / dealer123 (approved)")
        print("  Dealer: dealer002 / dealer123 (approved)")
        print("  Dealer: dealer003 / dealer123 (pending)")
        
    finally:
        await db.disconnect()


if __name__ == "__main__":
    asyncio.run(main())

