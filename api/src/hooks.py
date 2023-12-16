import asyncio
#from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from memcache import connection_and_init_memcached, close_memcached_connection
from db import connect_and_init_mongo, close_mongo_connect
from local_utils.elasticsearch_utils import connect_and_init_elasticsearch, close_connection_elasticsearch

# Запуск приложения
async def startup():
    #await connect_and_init_mongo()
    #await connect_and_init_elasticsearch()

    #Одновременный запуск mongodb и elasticsearch
    await asyncio.gather(connect_and_init_mongo(), connect_and_init_elasticsearch())
    connection_and_init_memcached()

# Выключение приложения
async def shutdown():
    #await close_mongo_connect()
    #await close_connection_elasticsearch()

    # Одновременный шутдаун mongodb и elasticsearch
    await asyncio.gather(close_mongo_connect(), close_connection_elasticsearch())
    close_memcached_connection()
