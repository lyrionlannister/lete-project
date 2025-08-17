from ..services.ConnectionService import ConnectionService

class ConnectionController:
    """
    Controller for managing database connections.
    """

    def __init__(self):
        self.service = ConnectionService.get_instance()

    async def get(self, id: int):
        return await self.service.get(id)

    async def get_all(self):
        return await self.service.get_all()

    async def create(self, data: dict):
        return await self.service.add(data)

    async def update(self, id: int, data: dict):
        return await self.service.update(id, data)

    async def delete(self, id: int):
        return await self.service.delete(id)