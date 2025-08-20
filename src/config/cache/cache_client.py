from dataclasses import dataclass
from typing import Optional, Any
from urllib.parse import urlparse
import redis.asyncio as redis
from .cache_config import CacheConfig

    
@dataclass
class CacheClient:

    def __init__(self, config: CacheConfig):
        self.config = config
        self.client: Optional[redis.Redis] = None

    async def connect(self):
        """Establece conexión con Redis usando la URL de configuración."""
        parsed_url = urlparse(self.config.url_connection)
        
        self.client = redis.Redis(
            host=parsed_url.hostname or 'localhost',
            port=parsed_url.port or 6379,
            db=int(parsed_url.path.lstrip('/')) if parsed_url.path else 0,
            password=parsed_url.password,
            decode_responses=False  
        )
        await self.client.ping()

    async def get(self, key: str) -> Optional[bytes]:
        """Obtiene un valor del cache."""
        if not self.client:
            await self.connect()
        return await self.client.get(key)

    async def set(self, key: str, value: Any, ex: Optional[int] = None) -> bool:
        """Establece un valor en el cache con expiración opcional."""
        if not self.client:
            await self.connect()
        return await self.client.set(key, value, ex=ex)

    async def delete(self, key: str) -> int:
        """Elimina una clave del cache."""
        if not self.client:
            await self.connect()
        return await self.client.delete(key)
    
    async def exists(self, key: str) -> bool:
        """Verifica si una clave existe."""
        if not self.client:
            await self.connect()
        return bool(await self.client.exists(key))
    
    async def ping(self) -> str:
        """Hace ping al servidor Redis para verificar la conexión."""
        if not self.client:
            await self.connect()
        result = await self.client.ping()
        return "pong" if result else "no response"
    
    async def close(self):
        """Cierra la conexión."""
        if self.client:
            await self.client.close()



