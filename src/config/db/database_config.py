from typing import TypedDict, Literal, Optional

class DatabaseConfig(TypedDict):
    host: str
    port: int
    user: str
    password: str
    database: Optional[str]
    ssl_enabled: bool
    db_engine: Literal['postgresql', 'mysql', 'sqlite', 'sqlserver']