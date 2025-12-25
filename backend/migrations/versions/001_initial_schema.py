"""Initial schema with users table placeholder

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create users table (placeholder for Phase 2)
    op.execute("""
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
    
    # Create dealers table (placeholder for Phase 2)
    op.execute("""
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
    
    # Create products table (placeholder for Phase 2)
    op.execute("""
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
    
    # Create orders table (placeholder for Phase 2)
    op.execute("""
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
    
    # Create order_items table (placeholder for Phase 2)
    op.execute("""
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


def downgrade():
    op.execute("DROP TABLE IF EXISTS order_items")
    op.execute("DROP TABLE IF EXISTS orders")
    op.execute("DROP TABLE IF EXISTS products")
    op.execute("DROP TABLE IF EXISTS dealers")
    op.execute("DROP TABLE IF EXISTS users")

