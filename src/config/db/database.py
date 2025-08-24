from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from .database_config import DatabaseConfig
from config.app.logger import Logger

class Database:

    _logger = Logger.get_logger()

    def __init__(self, config: DatabaseConfig):
        self.config = config
        self.engine = None
        self.session_factory = None

    async def connect(self):
        self._logger.info(f"Connecting to the database {self.config['database']}...")
        if not self.engine:
            conn_str = await self._get_db_connection_string()
            self.engine = create_async_engine(
                conn_str,
                echo=False,
                future=True
            )
            self.session_factory = async_sessionmaker(
                bind=self.engine,
                expire_on_commit=False,
                class_=AsyncSession
            )

    async def disconnect(self):
        if self.engine:
            self._logger.info(f"Disconnecting from the database {self.config['database']}...")
            await self.engine.dispose()
            self.engine = None
            self.session_factory = None

    @asynccontextmanager
    async def get_session(self):
        if not self.session_factory:
            await self.connect()

        async with self.session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception as e:
                await session.rollback()
                self._logger.error(f"Session rollback because of: {e}")
                raise

    async def _get_db_connection_string(self) -> str:
        ssl_mode = 'require' if self.config.get('ssl_enabled', False) else 'disable'
        sql_engine = self.config.get('db_engine', 'postgresql')

        match sql_engine:
            case 'sqlite':
                self._logger.info("Using SQLite database engine.")
                return f"sqlite+aiosqlite:///{self.config['database']}"
            case 'mysql':
                self._logger.info("Using MySQL database engine.")
                return (
                    f"mysql+aiomysql://{self.config['user']}:{self.config['password']}"
                    f"@{self.config['host']}:{self.config['port']}/{self.config['database']}"
                )
            case 'sqlserver':
                self._logger.info("Using SQL Server database engine.")
                return (
                    f"mssql+pyodbc://{self.config['user']}:{self.config['password']}"
                    f"@{self.config['host']}:{self.config['port']}/{self.config['database']}"
                    "?driver=ODBC+Driver+17+for+SQL+Server"
                )
            case 'postgresql':
                self._logger.info("Using PostgreSQL database engine.")

                
                if self.config.get('database') is None:
                    return (
                        f"postgresql+asyncpg://{self.config['user']}:{self.config['password']}"
                        f"@{self.config['host']}:{self.config['port']}"
                    )
                
                return (
                    f"postgresql+asyncpg://{self.config['user']}:{self.config['password']}"
                    f"@{self.config['host']}:{self.config['port']}/{self.config['database']}"
                )
            case _:
                raise ValueError(f"Unsupported database engine: {sql_engine}")
