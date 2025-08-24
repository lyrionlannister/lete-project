# from config.cache import *
# from modules.database.models import *

# class CacheUpdatedService:
    

#     def __init__ (self, cache_client: CacheClient):
#         self.cache_client = cache_client


#     async def save_cache(self, model: CachedTablesModel, data: dict) -> bool:
#         """
#         Guarda datos en el cache.
#         """
#         key = f"{model.table_name}:{model.primary_key}"
#         value = json.dumps(data)
        
#         return await self.cache_client.set(key, value, ex=model.expiration_time)
