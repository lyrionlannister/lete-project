from sqlalchemy import text

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

SQL_DATABASES_COMMANDS = {
    "postgresql": (text("SELECT datname FROM pg_database WHERE datistemplate = false;"), 0),
    "mysql": (text("SHOW DATABASES;"), 0),
    "sqlite": (text("PRAGMA database_list;"), 1),  # columna 1 = name
    "sqlserver": (text("SELECT name FROM sys.databases;"), 0),
    "oracle": (text("SELECT name FROM v$database;"), 0),
}

SQL_TABLES_COMMANDS = {
    "postgresql": """
        SELECT 
            table_schema,
            table_name
        FROM information_schema.tables
        WHERE table_type = 'BASE TABLE'
        AND table_schema = 'public'
        ORDER BY table_schema, table_name;
    """,
    "mysql": "SHOW TABLES;",
    "sqlite": "SELECT name FROM sqlite_master WHERE type='table';",
    "sqlserver": """
        SELECT TABLE_SCHEMA, TABLE_NAME
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_TYPE = 'BASE TABLE';
    """,
    "oracle": "SELECT table_name FROM user_tables;",
}
