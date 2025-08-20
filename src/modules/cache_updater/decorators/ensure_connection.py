from functools import wraps
from config.app.logger import Logger




def ensure_connection(func):
    """Decorator to ensure Redis connection before executing a function."""
    _logger = Logger.get_logger()

    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        if not self.client:
            try:
                _logger.info("Cliente de redis no se ha conectado... intentando reconectar.")
                await self.connect()
                _logger.info("Cliente de redis conectado.")
            except Exception as e:
                _logger.error(f"Error al conectar con Redis: {e}")
                # return "error"

        return await func(self, *args, **kwargs)

    return wrapper

