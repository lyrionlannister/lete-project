

# class CacheUpdatedService:


#     def __init__(self, cache_client):
#         self.cache_client = cache_client

    
#     async def update_cache(self, key: str, value: any, expiration: int = 3600 * 24) -> bool:
#         """Actualiza o establece un valor en el cache con una expiración predeterminada de 24 horas."""
#         return await self.cache_client.set(key, value, ex=expiration)