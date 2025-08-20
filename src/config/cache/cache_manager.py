import json
import pickle
from datetime import datetime, timedelta
from typing import Any, Optional, Dict, List
from urllib.parse import urlparse

from .cache_client import CacheClient
from .cache_config import CacheConfig
from config.app.logger import Logger


class CacheManager:
    """
    Gestor principal de cache que coordina las operaciones de Redis
    y maneja la configuración de cache para el sistema.
    """
    
    _instance = None
    _logger = Logger.get_logger()
    
    def __init__(self, config: Optional[CacheConfig] = None):
        if config is None:
            config = CacheConfig()
        
        self.config = config
        self.client = CacheClient(config)
        self._is_connected = False
        self._cache_stats = {
            "hits": 0,
            "misses": 0,
            "sets": 0,
            "deletes": 0
        }
    
    @classmethod
    def get_instance(cls, config: Optional[CacheConfig] = None):
        """
        Obtiene la instancia singleton del CacheManager.
        
        Args:
            config: Configuración opcional para inicializar la instancia
            
        Returns:
            CacheManager: Instancia singleton del manager
        """
        if not hasattr(cls, '_instance') or cls._instance is None:
            cls._instance = cls(config)
        return cls._instance
    
    async def connect(self) -> None:
        """
        Establece conexión con Redis.
        """
        try:
            await self.client.connect()
            self._is_connected = True
            self._logger.info("Cache Manager connected to Redis successfully")
        except Exception as e:
            self._logger.error(f"Failed to connect to Redis: {e}")
            self._is_connected = False
            raise
    
    async def disconnect(self) -> None:
        """
        Cierra la conexión con Redis.
        """
        try:
            if self.client.client:
                await self.client.client.close()
            self._is_connected = False
            self._logger.info("Cache Manager disconnected from Redis")
        except Exception as e:
            self._logger.error(f"Error disconnecting from Redis: {e}")
    
    async def get(self, key: str, deserialize: bool = True) -> Any:
        """
        Obtiene un valor del cache.
        
        Args:
            key: Clave del cache
            deserialize: Si deserializar el valor automáticamente
            
        Returns:
            Any: Valor del cache o None si no existe
        """
        try:
            if not self._is_connected:
                await self.connect()
            
            value = await self.client.get(key)
            
            if value is None:
                self._cache_stats["misses"] += 1
                return None
            
            self._cache_stats["hits"] += 1
            
            if deserialize:
                try:
                    # Intentar deserializar como JSON primero
                    return json.loads(value.decode('utf-8'))
                except (json.JSONDecodeError, UnicodeDecodeError):
                    try:
                        # Si falla JSON, intentar pickle
                        return pickle.loads(value)
                    except:
                        # Si todo falla, devolver como string
                        return value.decode('utf-8', errors='ignore')
            
            return value
            
        except Exception as e:
            self._logger.error(f"Error getting cache key '{key}': {e}")
            self._cache_stats["misses"] += 1
            return None
    
    async def set(self, key: str, value: Any, expiration: Optional[int] = None, 
                  serialize: bool = True) -> bool:
        """
        Establece un valor en el cache.
        
        Args:
            key: Clave del cache
            value: Valor a almacenar
            expiration: Tiempo de expiración en segundos (opcional)
            serialize: Si serializar el valor automáticamente
            
        Returns:
            bool: True si se almacenó correctamente
        """
        try:
            if not self._is_connected:
                await self.connect()
            
            # Preparar el valor para almacenamiento
            if serialize:
                if isinstance(value, (dict, list, tuple)):
                    serialized_value = json.dumps(value, default=str)
                elif isinstance(value, (int, float, bool)):
                    serialized_value = json.dumps(value)
                elif isinstance(value, str):
                    serialized_value = value
                else:
                    # Para objetos complejos usar pickle
                    serialized_value = pickle.dumps(value)
            else:
                serialized_value = value
            
            # Usar tiempo de expiración por defecto si no se especifica
            exp_time = expiration or self.config.expiration_time
            
            await self.client.set(key, serialized_value)
            
            # Establecer expiración si se especifica
            if exp_time > 0:
                await self.client.client.expire(key, exp_time)
            
            self._cache_stats["sets"] += 1
            self._logger.debug(f"Cache set: {key} (expires in {exp_time}s)")
            return True
            
        except Exception as e:
            self._logger.error(f"Error setting cache key '{key}': {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """
        Elimina una clave del cache.
        
        Args:
            key: Clave a eliminar
            
        Returns:
            bool: True si se eliminó correctamente
        """
        try:
            if not self._is_connected:
                await self.connect()
            
            result = await self.client.delete(key)
            self._cache_stats["deletes"] += 1
            self._logger.debug(f"Cache deleted: {key}")
            return bool(result)
            
        except Exception as e:
            self._logger.error(f"Error deleting cache key '{key}': {e}")
            return False
    
    async def exists(self, key: str) -> bool:
        """
        Verifica si una clave existe en el cache.
        
        Args:
            key: Clave a verificar
            
        Returns:
            bool: True si la clave existe
        """
        try:
            if not self._is_connected:
                await self.connect()
            
            result = await self.client.client.exists(key)
            return bool(result)
            
        except Exception as e:
            self._logger.error(f"Error checking existence of key '{key}': {e}")
            return False
    
    async def get_ttl(self, key: str) -> int:
        """
        Obtiene el tiempo de vida restante de una clave.
        
        Args:
            key: Clave a consultar
            
        Returns:
            int: TTL en segundos (-1 si no expira, -2 si no existe)
        """
        try:
            if not self._is_connected:
                await self.connect()
            
            return await self.client.client.ttl(key)
            
        except Exception as e:
            self._logger.error(f"Error getting TTL for key '{key}': {e}")
            return -2
    
    async def clear_pattern(self, pattern: str) -> int:
        """
        Elimina todas las claves que coinciden con un patrón.
        
        Args:
            pattern: Patrón de búsqueda (ej: "user:*")
            
        Returns:
            int: Número de claves eliminadas
        """
        try:
            if not self._is_connected:
                await self.connect()
            
            keys = await self.client.client.keys(pattern)
            if keys:
                deleted = await self.client.client.delete(*keys)
                self._cache_stats["deletes"] += deleted
                self._logger.info(f"Deleted {deleted} keys matching pattern '{pattern}'")
                return deleted
            return 0
            
        except Exception as e:
            self._logger.error(f"Error clearing pattern '{pattern}': {e}")
            return 0
    
    async def flush_all(self) -> bool:
        """
        Limpia todo el cache.
        
        Returns:
            bool: True si se limpió correctamente
        """
        try:
            if not self._is_connected:
                await self.connect()
            
            await self.client.client.flushdb()
            self._logger.info("Cache flushed successfully")
            return True
            
        except Exception as e:
            self._logger.error(f"Error flushing cache: {e}")
            return False
    
    async def get_cache_info(self) -> Dict[str, Any]:
        """
        Obtiene información del estado del cache.
        
        Returns:
            Dict: Información del cache
        """
        try:
            if not self._is_connected:
                await self.connect()
            
            info = await self.client.client.info()
            
            return {
                "connected": self._is_connected,
                "redis_version": info.get("redis_version"),
                "used_memory": info.get("used_memory_human"),
                "connected_clients": info.get("connected_clients"),
                "total_commands_processed": info.get("total_commands_processed"),
                "keyspace": info.get("db0", {}),
                "stats": self._cache_stats,
                "config": {
                    "cache_size": self.config.cache_size,
                    "expiration_time": self.config.expiration_time,
                    "url_connection": self.config.url_connection
                }
            }
            
        except Exception as e:
            self._logger.error(f"Error getting cache info: {e}")
            return {
                "connected": False,
                "error": str(e),
                "stats": self._cache_stats
            }
    
    async def health_check(self) -> bool:
        """
        Verifica la salud de la conexión al cache.
        
        Returns:
            bool: True si el cache está funcionando correctamente
        """
        try:
            if not self._is_connected:
                await self.connect()
            
            # Hacer un ping a Redis
            pong = await self.client.client.ping()
            return pong is True
            
        except Exception as e:
            self._logger.error(f"Cache health check failed: {e}")
            return False
    
    def get_stats(self) -> Dict[str, int]:
        """
        Obtiene estadísticas de uso del cache.
        
        Returns:
            Dict: Estadísticas de cache
        """
        hit_rate = 0
        total_requests = self._cache_stats["hits"] + self._cache_stats["misses"]
        if total_requests > 0:
            hit_rate = (self._cache_stats["hits"] / total_requests) * 100
        
        return {
            **self._cache_stats,
            "hit_rate_percentage": round(hit_rate, 2),
            "total_requests": total_requests
        }