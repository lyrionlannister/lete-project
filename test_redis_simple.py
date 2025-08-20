#!/usr/bin/env python3
"""
Script de prueba simple para verificar la conexión con Redis.
Este script prueba directamente la conexión sin depender de otros módulos del proyecto.
"""

import asyncio
import redis.asyncio as redis


async def test_redis_ping_simple():
    """Prueba simple de conexión con Redis usando ping."""
    print("🔄 Iniciando prueba simple de conexión con Redis...")
    
    try:
        # Crear conexión directa a Redis
        client = redis.Redis(
            host='localhost',
            port=6379,
            db=0,
            password='InnovalTech',
            decode_responses=False
        )
        
        print("📡 Conectando a redis://:****@localhost:6379/0")
        
        # Realizar ping
        response = await client.ping()
        
        if response:
            print("✅ ¡Conexión exitosa! Redis respondió: 'pong'")
            print(f"🔍 Respuesta raw: {response} (tipo: {type(response)})")
            
            # Probar operaciones básicas
            print("\n🧪 Probando operaciones básicas...")
            
            # Set
            await client.set("test_key", "test_value", ex=60)
            print("✅ Valor guardado exitosamente")
            
            # Get
            value = await client.get("test_key")
            print(f"✅ Valor recuperado: {value}")
            
            # Exists
            exists = await client.exists("test_key")
            print(f"✅ La clave existe: {bool(exists)}")
            
            # Delete
            deleted = await client.delete("test_key")
            print(f"✅ Claves eliminadas: {deleted}")
            
            await client.close()
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


async def main():
    """Función principal."""
    print("🚀 Prueba simple de conexión Redis")
    print("=" * 40)
    
    success = await test_redis_ping_simple()
    
    if success:
        print("\n🎉 ¡Prueba exitosa! El cliente Redis funciona correctamente.")
        return 0
    else:
        print("\n❌ La prueba falló.")
        print("\n💡 Para verificar Redis:")
        print("   redis-cli ping")
        print("   sudo systemctl status redis-server")
        return 1


if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Prueba interrumpida por el usuario")
        exit(130)
