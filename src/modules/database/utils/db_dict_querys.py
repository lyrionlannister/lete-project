SQL_DATABASES_COMMANDS = {
    "postgresql": "SELECT datname FROM pg_database WHERE datistemplate = false;",
    "mysql": "SHOW DATABASES;",
    "sqlite": "PRAGMA database_list;",
    "sqlserver": "SELECT name FROM sys.databases;",
    "oracle": "SELECT name FROM v$database;",
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
