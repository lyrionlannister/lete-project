import os


from .database import Database
from .database_config import DatabaseConfig

lete_config = DatabaseConfig(
    host=os.getenv("DB_HOST_PGSQL"),
    port=os.getenv("DB_PORT_PGSQL"),
    user=os.getenv("USER_PGSQL"),
    password=os.getenv("PASSWORD_PGSQL"),
    database=os.getenv("DB_NAME_PGSQL"),
    ssl_enabled=os.getenv("SSL_ENABLED_PGSQL"),
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


