import asyncio
import sys
import os
from sqlalchemy import text  # ✅ Import text function

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_connection():
    try:
        # Test 1: Import models
        from app import models
        print("✅ Models imported successfully")
        
        # Test 2: Check Base metadata
        from app.database import Base
        print(f"📊 Tables in metadata: {list(Base.metadata.tables.keys())}")
        
        # Test 3: Database connection
        from app.database import engine
        
        async with engine.connect() as conn:
            # ✅ Use text() function for raw SQL
            result = await conn.execute(text("SELECT version()"))
            db_version = result.fetchone()
            print(f"✅ PostgreSQL connected: {db_version[0]}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_connection())