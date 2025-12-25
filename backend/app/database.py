import asyncpg
from typing import Optional
from contextlib import asynccontextmanager

from app.config import settings


class Database:
    """Database connection pool manager."""
    
    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None
    
    async def connect(self):
        """Create connection pool."""
        if self.pool is None:
            self.pool = await asyncpg.create_pool(
                settings.database_url,
                min_size=2,
                max_size=10,
            )
    
    async def disconnect(self):
        """Close connection pool."""
        if self.pool:
            await self.pool.close()
            self.pool = None
    
    @asynccontextmanager
    async def connection(self):
        """Get a connection from the pool."""
        if self.pool is None:
            raise RuntimeError("Database not connected")
        async with self.pool.acquire() as conn:
            yield conn
    
    async def execute(self, query: str, *args):
        """Execute a query."""
        async with self.connection() as conn:
            return await conn.execute(query, *args)
    
    async def fetch(self, query: str, *args):
        """Fetch multiple rows."""
        async with self.connection() as conn:
            return await conn.fetch(query, *args)
    
    async def fetchrow(self, query: str, *args):
        """Fetch a single row."""
        async with self.connection() as conn:
            return await conn.fetchrow(query, *args)
    
    async def fetchval(self, query: str, *args):
        """Fetch a single value."""
        async with self.connection() as conn:
            return await conn.fetchval(query, *args)


# Global database instance
db = Database()

