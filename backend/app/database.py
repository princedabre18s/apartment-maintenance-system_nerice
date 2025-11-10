from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from typing import AsyncGenerator
from .config import settings

# Create async engine
engine = create_async_engine(
    settings.database_url,
    echo=True,
    future=True
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# Base class for models
Base = declarative_base()


class Database:
    @classmethod
    async def connect_db(cls):
        """
        Initialize database connection and create tables.
        """
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print(f"Connected to PostgreSQL: {settings.pg_database}")
        
    @classmethod
    async def close_db(cls):
        """
        Close database connection.
        """
        await engine.dispose()
        print("Closed PostgreSQL connection")


# Dependency to get DB session
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
