from typing import TypedDict, Literal

class DatabaseConfig(TypedDict):
    host: str
    port: int
    user: str
    password: str
    database: str
    ssl_enabled: bool
    db_engine: Literal['postgresql', 'mysql', 'sqlite', 'sqlserver']