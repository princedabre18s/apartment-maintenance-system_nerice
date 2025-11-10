"""
Initialize PostgreSQL database - create all tables.
Run this script once before seeding data.
"""
import asyncio
from app.database import engine, Base
from app.models.db_models import Building, Unit, Tenant, Staff, Request

async def init_db():
    """Create all tables in the database."""
    print("Creating database tables...")
    async with engine.begin() as conn:
        # Drop all tables (use carefully!)
        # await conn.run_sync(Base.metadata.drop_all)
        
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
    
    print("✅ Database tables created successfully!")

if __name__ == "__main__":
    asyncio.run(init_db())
