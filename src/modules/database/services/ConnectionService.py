
from ..models import ConnectionModel
from base.service.base_service import BaseService
from config.db import *

class ConnectionService(BaseService):
    
    @classmethod
    def get_instance(cls):
        """
        Returns an instance of the ConnectionService.
        """
        if not hasattr(cls, '_instance'):
            db = get_app_db()
            cls._instance = cls(db, ConnectionModel)
        
        return cls._instance

   