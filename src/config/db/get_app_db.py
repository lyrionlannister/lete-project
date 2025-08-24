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

server_config = (
    DatabaseConfig(
        host=os.getenv("DB_HOST_MYSQL"),
        port=os.getenv("DB_PORT_MYSQL"),
        user=os.getenv("USER_MYSQL"),
        password=os.getenv("PASSWORD_MYSQL"),
        database=None,
        ssl_enabled=os.getenv("SSL_ENABLED_MYSQL"),
        db_engine="mysql"
    )
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



async def get_server_db() -> Database:
    """
    Returns the server database instance.
    """
    db = None
    if not db:
        db = Database(server_config)
        await db.connect()
    return db