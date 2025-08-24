
from ..models import ConnectionModel
from modules.base import BaseService
from config.db import *
from . import *

class ConnectionService(BaseService):
    

    def __init__(self, db, model):
        super().__init__(db, model)


    @classmethod
    async def get_instance(cls):
        """
        Returns an instance of the ConnectionService.
        """
        if not hasattr(cls, '_instance'):
            db = await get_app_db()
            cls._instance = cls(db, ConnectionModel)
        
        return cls._instance
    
    # async create_connection(self, config: dict) ->