from ..services.connection_service import ConnectionService
from modules.base.controller.base_controller import BaseController

class ConnectionController(BaseController):
    """
    Controller for managing database connections.
    Inherits from BaseController to provide common functionality.
    """

    def __init__(self, service):
        super().__init__(service)

    @classmethod
    async def get_instance(cls):
        if not hasattr(cls, "_instance"):
            service = await ConnectionService.get_instance()
            cls._instance = cls(service)
        return cls._instance

    async def get_connection(self, id: int):
        """
        Retrieves a connection by its ID.

        :param id: The ID of the connection to retrieve
        """
        
        return await self.get(id)

    async def get_all_connections(self):
        """
        Retrieves all connections.

        :return: List of all connections
        """
        return await self.get_all()
    
    async def create_connection(self, data: dict):
        """
        Creates a new connection.

        :param data: The data for the new connection
        """
        return await self.create(data)
    
    async def update_connection(self, id: int, data: dict):
        """
        Updates an existing connection.

        :param id: The ID of the connection to update
        :param data: The new data for the connection
        """
        return await self.update(id, data)
    
    async def delete_connection(self, id: int):
        """
        Deletes a connection by its ID.

        :param id: The ID of the connection to delete
        """
        return await self.delete(id)