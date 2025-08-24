from fastapi import FastAPI
from dotenv import load_dotenv

from modules.database import database_router
from modules.database.models import *
from config.db import *
from config.cache import *




load_dotenv()

app = FastAPI(root_path="/api")

app.include_router(database_router, prefix="/database", tags=["database"])

app = FastAPI(root_path="/api")

async def test_cache_connection():
    """Test the cache connection on startup."""
    cache_client = CacheClient(CacheConfig())
    try:
        # await cache_client.connect()
        print(await cache_client.ping())
        print("✅ Cache connection established successfully.")
    except Exception as e:
        print(f"Failed to connect to cache: {e}")
    finally:
        await cache_client.close()

@app.on_event("startup")
async def on_startup():
    db = await get_app_db()
    server_conn = await get_server_db()
    print(await server_conn._get_db_connection_string())
    dinamic_model_factory = await DinamicModelFactory.get_instance()
    databases = await dinamic_model_factory.get_databases(server_conn.engine, "postgresql")
    tables = await dinamic_model_factory.get_tables(db.engine)
    fields = await dinamic_model_factory.get_table_columns(db.engine, "connections")

    print(f"Databases available: {databases}")
    print(f"Tables available: {tables}")
    print(f"Fields in 'connections' table: {fields}")

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
