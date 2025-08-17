from fastapi import FastAPI

from modules.database import database_router
from modules.database.models import *
from config.db import Base, get_app_db

app = FastAPI(root_path="/api")

app.include_router(database_router, prefix="/database", tags=["database"])

@app.on_event("startup")
async def on_startup():
    db = await get_app_db()
    await db.connect()
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
