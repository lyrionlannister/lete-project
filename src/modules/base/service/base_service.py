import pandas as pd
from sqlalchemy import text, TextClause
from typing import TypeVar

from sqlalchemy.orm import DeclarativeBase
from config.app.logger import Logger
from config.db.database import Database


Model = TypeVar('Model', bound=DeclarativeBase)

class BaseService:
    _logger = Logger.get_logger()

    def __init__(self, db: Database, model: Model):
        self.db = db
        self.model = model

    async def add(self, data: dict) -> Model:
        """
        Adds a new model instance to the database.

        :param model: The model instance to add
        """
        try:
            new_record = self.model(**data)
            async with self.db.get_session() as session:
                session.add(new_record)
                await session.commit()
                await session.refresh(new_record)
                self._logger.info(f"Added new record: {new_record}")
        except Exception as e:
            self._logger.error(f"BaseService.add Error: {e}")
            raise Exception(f"BaseService.add Error: {e}")
            
        
    async def get(self, id: int) -> Model:
        """
        Retrieves a model instance from the database by its ID.

        :param id: The ID of the model instance to retrieve
        """
        try:
            async with self.db.get_session() as session:
                return await session.get(self.model, id)
        except Exception as e:
            self._logger.error(f"BaseService.get Error: {e}")
            raise Exception(f"BaseService.get Error: {e}")
        
    async def get_all(self) -> pd.DataFrame:
        try:
            query = text(f"SELECT * FROM {self.model.__tablename__}")
            async with self.db.engine.connect() as conn:
                try:
                    data = await conn.run_sync(lambda sync_conn: pd.read_sql(query, sync_conn, dtype_backend='pyarrow'))
                    print(data)
                    return data
                except Exception as e:
                    self._logger.error(f"Error executing query: {e}")
                    raise Exception(f"Error executing query: {e}")
                finally:
                    await conn.close()
        except Exception as e:
            self._logger.error(f"BaseService.get_all Error: {e}")
            raise Exception(f"BaseService.get_all Error: {e}")

    async def update(self, id: int, data: dict) -> Model:
        """
        Updates a model instance in the database.

        :param id: The ID of the model instance to update
        :param data: The data to update the model instance with
        """
        try:
            async with self.db.get_session() as session:
                record = await session.get(self.model, id)
                if not record:
                    raise ValueError("Not Found")
                
                for key, value in data.items():
                    setattr(record, key, value)
                await session.commit()
                await session.refresh(record)
                self._logger.info(f"Updated record: {record}")
                return record
        except Exception as e:
            self._logger.error(f"BaseService.update Error: {e}")
            raise Exception(f"BaseService.update Error: {e}")
        

    
    async def get_by_query(self, query: TextClause) -> pd.DataFrame:
        """
        Retrieves data from the database based on a custom SQL query.

        :param query: The SQL query to execute
        :return: DataFrame containing the results of the query
        """
        try:
            async with self.db.engine.connect() as conn:
                data = await conn.run_sync(lambda sync_conn: pd.read_sql(query, sync_conn, dtype_backend='pyarrow'))
                print(data)
                return data
        except Exception as e:
            self._logger.error(f"BaseService.get_by_query Error: {e}")
            raise Exception(f"BaseService.get_by_query Error: {e}")
        
    async def delete(self, id: int) -> bool:
        """
        Deletes a model instance from the database.

        :param id: The ID of the model instance to delete
        """
        try:
            async with self.db.get_session() as session:
                try:
                    record = await session.get(self.model, id)
                    if record:
                        await session.delete(record)
                        await session.commit()
                        self._logger.info(f"Deleted record with id: {id}")
                        return True
                    else:
                        raise ValueError(f"Record with id {id} not found.")
                except Exception as e:
                    self._logger.error(f"Error deleting record with id {id}: {e}")
                    raise Exception(f"Error deleting record with id {id}: {e}")
                finally:
                    await session.close()
        except Exception as e:
            self._logger.error(f"BaseService.delete Error: {e}")
            raise Exception(f"BaseService.delete Error: {e}")