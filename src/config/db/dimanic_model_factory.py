from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import inspect, MetaData, Table
from modules.database.utils.db_dict_querys import *


class DinamicModelFactory:
    """
    Factory class for creating dynamic models.
    This class is responsible for generating models based on the provided configuration.
    """

    @classmethod
    async def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls()
        return cls._instance
    

    async def get_databases(self, engine: AsyncEngine, sql_manager: str) -> list[str]:
        """
        Retrieve the list of databases from the provided SQLAlchemy engine.
        """
        entry = SQL_DATABASES_COMMANDS.get(sql_manager)
        if entry is None:
            raise ValueError(f"Unsupported SQL manager: {sql_manager}")

        query, col_index = entry

        try:
            async with engine.connect() as connection:
                result = await connection.execute(query)
                return [row[col_index] for row in result.fetchall()]
        except Exception as e:
            raise RuntimeError(f"Error retrieving databases: {e}")




    async def get_schemas(self, engine: AsyncEngine) -> list[str]:
        """
        Retrieve the list of databases from the provided SQLAlchemy engine.
        """


        try:
        
            async with engine.connect() as connection:
                return await connection.run_sync(lambda sync_conn: inspect(sync_conn).get_schema_names())
        except Exception as e:
            raise RuntimeError(f"Error retrieving databases: {e}")
        
    async def get_tables(self, engine: AsyncEngine) -> list[str]:

        try:
            async with engine.connect() as connection:
                result = await connection.run_sync(lambda sync_conn: inspect(sync_conn).get_table_names())
                return [table for table in result]
        except Exception as e:
            raise RuntimeError(f"Error retrieving tables: {e}")
        


    async def get_table_columns(self, engine: AsyncEngine, table_name: str) -> list[str]:
        try:
            async with engine.connect() as connection:
                def sync_reflect(sync_conn):
                    metadata = MetaData()
                    metadata.reflect(bind=sync_conn, only=[table_name])
                    table = metadata.tables[table_name]
                    # print(table.columns)

                    return [{
                        "name": column.name,
                        "type": str(column.type),
                        "nullable": column.nullable,
                        "default": column.default.arg if column.default else None
                    } for column in table.columns
                    ]

                return await connection.run_sync(sync_reflect)

        except Exception as e:
            raise RuntimeError(f"Error retrieving columns for table {table_name}: {e}")