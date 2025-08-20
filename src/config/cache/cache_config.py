import os
from dataclasses import dataclass

@dataclass
class CacheConfig:
    cache_size: int = 1024 * 1024 * 1024  # Default to 1GB
    expiration_time: int = 3600 * 24  # Default to 24 hours
    url_connection: str = os.getenv("REDIS_URL")







    