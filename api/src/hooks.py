import asyncio
#from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from memcache import connection_and_init_memcached, close_memcached_connection
from db import connect_and_init_mongo, close_mongo_connect
from local_utils.elasticsearch_utils import connect_and_init_elasticsearch, close_connection_elasticsearch


async def startup():
    init_mongo_future = connect_and_init_mongo()
    init_elasticsearch_future = connect_and_init_elasticsearch()

    #Одновременный запуск mongodb и elasticsearch
    await asyncio.gather(init_mongo_future, init_elasticsearch_future)
    connection_and_init_memcached()

async def shutdown():
    close_mongo_connect()
    close_memcached_connection()
    await close_connection_elasticsearch()
