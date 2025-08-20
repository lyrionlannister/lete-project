from fastapi import FastAPI

from modules.database.models import *
from config.db import Base, get_app_db
from config.cache import *

app = FastAPI(root_path="/api")

async def test_cache_connection():
    """Test the cache connection on startup."""
    cache_client = CacheClient(CacheConfig())
    try:
        await cache_client.connect()
        print(await cache_client.ping())
        print("✅ Cache connection established successfully.")
    except Exception as e:
        print(f"Failed to connect to cache: {e}")
    finally:
        await cache_client.close()

@app.on_event("startup")
async def on_startup():
    db = await get_app_db()
    await db.connect()
    await test_cache_connection()
    # Create tables if they do not exist
    async with db.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("shutdown")
async def on_shutdown():
    db = await get_app_db()
    await db.disconnect()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI application!"}
