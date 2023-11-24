import asyncio
#from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
#from cache.memcached_utils import connect_and_init_memcached, close_memcached_connect
from db import connect_and_init_mongo, close_mongo_connect
#from elasticsearch_utils import connect_and_init_elasticsearch, close_elasticsearch_connect

def connect_and_init_elasticsearch():
    pass

async def startup():
    await connect_and_init_mongo()
    #init_elasticsearch_future = connect_and_init_elasticsearch()
    #asyncio.gather(init_mongo_future, init_elasticsearch_future)
    #connect_and_init_memcached()


async def shutdown():
    close_mongo_connect()
    #close_memcached_connect()
    #await close_elasticsearch_connect()
