from typing import TypeVar
from fastapi import HTTPException

from config.app import *
from ..service.base_service import BaseService

Service = TypeVar('Service', bound=BaseService)

class BaseController:
    """
    Base controller class that provides common functionality for all controllers.
    """

    _logger = Logger.get_logger()
    def __init__(self, service: Service):
        self.service = service

    async def get(self, id: int):
        """
        Retrieves a model instance by its ID.

        :param id: The ID of the model instance to retrieve
        """
        try:
            data = await self.service.get(id)
            if data is None:
                raise HTTPException(status_code=404, detail="Record not found")
            
            return await make_api_response(
                success=True,
                status_code=200,
                data=data,
                message="Record retrieved successfully"
            )
        except Exception as e:
            self._logger.error(f"BaseController.get Error: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        
    async def get_all(self):
        """
        Retrieves all model instances.

        :return: List of all model instances
        """
        try:
            return await self.service.get_all()
        except Exception as e:
            self._logger.error(f"BaseController.get_all Error: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        
    async def create(self, data: dict):
        """
        Creates a new model instance.

        :param data: The data for the new model instance
        """
        try:
            return await self.service.add(data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    async def update(self, id: int, data: dict):
        """
        Updates an existing model instance.

        :param id: The ID of the model instance to update
        :param data: The new data for the model instance
        """
        try:
            return await self.service.update(id, data)
        except Exception as e:
            self._logger.error(f"BaseController.update Error: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def delete(self, id: int):
        """
        Deletes a model instance by its ID.

        :param id: The ID of the model instance to delete
        """
        try:
            return await self.service.delete(id)
        except Exception as e:
            self._logger.error(f"BaseController.delete Error: {e}")
            raise HTTPException(status_code=500, detail=str(e))