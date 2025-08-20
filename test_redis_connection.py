#!/usr/bin/env python3
"""
Script de prueba para verificar la conexión con Redis.
Ejecuta un ping para comprobar que el cliente responde "pong".
"""

import asyncio
import sys
import os

# Agregar el directorio src al path para importar los módulos
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.config.cache.cache_config import CacheConfig
from src.config.cache.cache_client import CacheClient


async def test_redis_ping():
    """Prueba la conexión con Redis usando el método ping."""
    print("🔄 Iniciando prueba de conexión con Redis...")
    
    try:
        # Crear configuración por defecto
        config = CacheConfig()
        print(f"📡 Conectando a: {config.url_connection}")
        
        # Crear cliente de cache
        cache_client = CacheClient(config)
        
        # Realizar ping
        response = await cache_client.ping()
        
        if response == "pong":
            print("✅ ¡Conexión exitosa! Redis respondió: 'pong'")
            return True
        else:
            print(f"❌ Redis no respondió correctamente: '{response}'")
            return False
            
    except ConnectionError as e:
        print(f"❌ Error de conexión: {e}")
        print("💡 Asegúrate de que Redis esté ejecutándose en localhost:6379")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False
    finally:
        # Cerrar conexión si existe
        try:
            await cache_client.close()
            print("🔒 Conexión cerrada correctamente")
        except:
            pass


async def test_basic_operations():
    """Prueba operaciones básicas del cache."""
    print("\n🔄 Probando operaciones básicas del cache...")
    
    try:
        config = CacheConfig()
        cache_client = CacheClient(config)
        
        # Probar set
        test_key = "test_key"
        test_value = "test_value"
        
        await cache_client.set(test_key, test_value, ex=60)  # Expira en 60 segundos
        print(f"✅ Valor guardado: {test_key} = {test_value}")
        
        # Probar get
        retrieved_value = await cache_client.get(test_key)
        if retrieved_value:
            decoded_value = retrieved_value.decode('utf-8')
            print(f"✅ Valor recuperado: {test_key} = {decoded_value}")
        
        # Probar exists
        exists = await cache_client.exists(test_key)
        print(f"✅ La clave existe: {exists}")
        
        # Probar delete
        deleted = await cache_client.delete(test_key)
        print(f"✅ Claves eliminadas: {deleted}")
        
        # Verificar que se eliminó
        exists_after_delete = await cache_client.exists(test_key)
        print(f"✅ La clave existe después de eliminar: {exists_after_delete}")
        
        await cache_client.close()
        return True
        
    except Exception as e:
        print(f"❌ Error en operaciones básicas: {e}")
        return False


async def main():
    """Función principal que ejecuta todas las pruebas."""
    print("🚀 Iniciando pruebas del cliente Redis...")
    print("=" * 50)
    
    # Prueba de ping
    ping_success = await test_redis_ping()
    
    if ping_success:
        # Si el ping fue exitoso, probar operaciones básicas
        operations_success = await test_basic_operations()
        
        if operations_success:
            print("\n🎉 ¡Todas las pruebas pasaron exitosamente!")
            return 0
        else:
            print("\n⚠️  El ping funcionó pero hubo errores en las operaciones básicas")
            return 1
    else:
        print("\n❌ Error en la conexión inicial. Verifica que Redis esté ejecutándose.")
        print("\n💡 Para iniciar Redis:")
        print("   - Ubuntu/Debian: sudo systemctl start redis-server")
        print("   - macOS: brew services start redis")
        print("   - Docker: docker run -d -p 6379:6379 redis:latest")
        return 1


if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Prueba interrumpida por el usuario")
        sys.exit(130)
