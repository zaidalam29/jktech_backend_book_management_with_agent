# test_db_standalone.py
import asyncio
import sys
import os
from sqlalchemy import text

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_database():
    """Standalone database test"""
    try:
        print("=" * 50)
        print("🧪 DATABASE CONNECTION TEST")
        print("=" * 50)
        
        # Import required modules
        try:
            from app import models
            print("✅ Models imported successfully")
        except Exception as e:
            print(f"❌ Failed to import models: {e}")
            return False
        
        try:
            from app.database import Base, engine
            print("✅ Database modules imported successfully")
        except Exception as e:
            print(f"❌ Failed to import database modules: {e}")
            return False
        
        # List tables
        try:
            tables = list(Base.metadata.tables.keys())
            print(f"📊 Found {len(tables)} tables: {tables}")
        except Exception as e:
            print(f"❌ Failed to list tables: {e}")
            return False
        
        # Test connection
        try:
            async with engine.connect() as conn:
                # Simple test query
                result = await conn.execute(text("SELECT 1 as test_value"))
                row = result.fetchone()
                
                if row and row[0] == 1:
                    print("✅ Database connection test: PASSED")
                else:
                    print("❌ Database connection test: FAILED")
                    return False
                
                # Try to get more info
                try:
                    result = await conn.execute(text("SELECT current_database()"))
                    db_name = result.fetchone()[0]
                    print(f"📊 Connected to database: {db_name}")
                except:
                    pass
                    
                try:
                    result = await conn.execute(text("SELECT version()"))
                    version = result.fetchone()[0]
                    print(f"📊 Database version: {version}")
                except:
                    pass
                    
            return True
            
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            import traceback
            traceback.print_exc()
            return False
            
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function to run the test"""
    print("🚀 Starting database tests...")
    
    # Run the async test
    success = asyncio.run(test_database())
    
    print("=" * 50)
    if success:
        print("🎉 ALL DATABASE TESTS PASSED!")
    else:
        print("💥 SOME TESTS FAILED")
    print("=" * 50)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())