# recreate_db.py
import asyncio
from app.database import Base, engine
from app.models import Document, User, Book

async def recreate_database():
    async with engine.begin() as conn:
        # Drop all tables
        await conn.run_sync(Base.metadata.drop_all)
        # Create all tables with new schema
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Database recreated with new schema")

if __name__ == "__main__":
    asyncio.run(recreate_database())