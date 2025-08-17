from .database import Database
from .database_config import DatabaseConfig

lete_config = DatabaseConfig(
    host="localhost",
    port=5432,
    user="postgres",
    password="Admin369*",
    database="lete_db",
    ssl_enabled=False,
    db_engine="postgresql"
)


async def get_app_db() -> Database:
    """
    Returns the application database instance.
    """
    db = None
    if not db:
        db = Database(lete_config)
        await db.connect()
    return db


