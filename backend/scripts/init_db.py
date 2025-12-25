#!/usr/bin/env python3
"""Database initialization script.

Creates the database schema by running all migrations.
"""
import asyncio
import os
import sys

import asyncpg


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://xinyutian:xinyutian@localhost:5432/xinyutian"
)


async def init_database():
    """Initialize database with schema."""
    # Convert to asyncpg format
    db_url = DATABASE_URL.replace("postgresql://", "postgres://")
    
    print(f"Connecting to database...")
    
    try:
        conn = await asyncpg.connect(db_url)
        print("Connected successfully!")
        
        # Create alembic_version table if not exists
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS alembic_version (
                version_num VARCHAR(32) NOT NULL,
                CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
            )
        """)
        
        # Check current version
        current_version = await conn.fetchval(
            "SELECT version_num FROM alembic_version LIMIT 1"
        )
        
        if current_version:
            print(f"Database already initialized at version: {current_version}")
        else:
            print("Creating initial schema...")
            
            # Create users table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    username VARCHAR(100) UNIQUE NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    role VARCHAR(20) NOT NULL DEFAULT 'dealer',
                    is_active BOOLEAN NOT NULL DEFAULT true,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create dealers table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS dealers (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
                    company_name VARCHAR(255) NOT NULL,
                    contact_name VARCHAR(100) NOT NULL,
                    phone VARCHAR(20) NOT NULL,
                    address TEXT,
                    status VARCHAR(20) NOT NULL DEFAULT 'pending',
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create products table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    name VARCHAR(255) NOT NULL,
                    category VARCHAR(100) NOT NULL,
                    price DECIMAL(10, 2) NOT NULL,
                    unit VARCHAR(50) NOT NULL,
                    min_order_quantity INTEGER NOT NULL DEFAULT 1,
                    description TEXT,
                    image_url TEXT,
                    stock INTEGER NOT NULL DEFAULT 0,
                    is_active BOOLEAN NOT NULL DEFAULT true,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create orders table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    order_no VARCHAR(50) UNIQUE NOT NULL,
                    dealer_id UUID REFERENCES dealers(id) ON DELETE RESTRICT,
                    status VARCHAR(20) NOT NULL DEFAULT 'pending',
                    total_amount DECIMAL(12, 2) NOT NULL,
                    shipping_address TEXT NOT NULL,
                    notes TEXT,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create order_items table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS order_items (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    order_id UUID REFERENCES orders(id) ON DELETE CASCADE,
                    product_id UUID REFERENCES products(id) ON DELETE RESTRICT,
                    product_name VARCHAR(255) NOT NULL,
                    quantity INTEGER NOT NULL,
                    unit_price DECIMAL(10, 2) NOT NULL,
                    subtotal DECIMAL(12, 2) NOT NULL
                )
            """)
            
            # Record migration version
            await conn.execute(
                "INSERT INTO alembic_version (version_num) VALUES ($1)",
                "001"
            )
            
            print("Schema created successfully!")
        
        await conn.close()
        print("Database initialization complete.")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(init_database())

