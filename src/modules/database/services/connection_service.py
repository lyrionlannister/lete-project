
from ..models import ConnectionModel
from modules.base import BaseService
from config.db import *

class ConnectionService(BaseService):
    
    @classmethod
    async def get_instance(cls):
        """
        Returns an instance of the ConnectionService.
        """
        if not hasattr(cls, '_instance'):
            db = await get_app_db()
            cls._instance = cls(db, ConnectionModel)
        
        return cls._instance