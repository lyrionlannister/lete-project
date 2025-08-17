from fastapi import APIRouter
from ..controllers.connection_controller import ConnectionController

router = APIRouter()

@router.get("/connections/{id}")
async def get_connection(id: int):
    """
    Retrieves a connection by its ID.
    
    :param id: The ID of the connection to retrieve
    """
    controller = await ConnectionController.get_instance()
    return await controller.get_connection(id)

@router.get("/connections")
async def get_all_connections():
    """
    Retrieves all connections.
    
    :return: List of all connections
    """
    controller = await ConnectionController.get_instance()
    return await controller.get_all_connections()

@router.post("/connections")
async def create_connection(data: dict):
    """
    Creates a new connection.
    
    :param data: The data for the new connection
    """
    controller = await ConnectionController.get_instance()
    return await controller.create_connection(data)


@router.put("/connections/{id}")
async def update_connection(id: int, data: dict):
    """
    Updates an existing connection.
    
    :param id: The ID of the connection to update
    :param data: The new data for the connection
    """
    controller = await ConnectionController.get_instance()
    return await controller.update_connection(id, data)

@router.delete("/connections/{id}")
async def delete_connection(id: int):
    """
    Deletes a connection by its ID.
    
    :param id: The ID of the connection to delete
    """
    controller = await ConnectionController.get_instance()
    return await controller.delete_connection(id)