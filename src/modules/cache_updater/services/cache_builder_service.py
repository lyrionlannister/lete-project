
from config.db.database_base import Base
from typing import Optional, Any
from datetime import date, datetime
from modules.database.models import *

class CacheBuilderService:

    def build_key(model: type[CachedTablesModel], indentifier: Optional[Any] = None,  prefix: str = "cache", start_date: Optional[date] = None, end_date: Optional[date] = None, extra: Optional[Any] = None) -> str:
        
        model_name = model.table_name
        key_parts = [prefix, model_name]
        
        if indentifier is not None:
            key_parts.append(str(indentifier))

        if start_date and end_date:
            key_parts.append(f"from={CacheBuilderService._format_date(start_date)}")
            key_parts.append(f"to={CacheBuilderService._format_date(end_date)}")
        
        if extra is not None:
            key_parts.append(str(extra))
        
        return ":".join(key_parts)

    

    @staticmethod
    def _format_date(value: Any) -> str:
        if isinstance(value, (date, datetime)):
            return value.strftime("%Y%m%d")
        return str(value)