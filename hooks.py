#from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
#from cache.memcached_utils import connect_and_init_memcached, close_memcached_connect
from db import connect_and_init_mongo, close_mongo_connect
from elasticsearch.elasticsearch_utils import connect_elasticsearch_and_init, close_elasticsearch_connect


async def startup():
    await connect_and_init_mongo()
    await connect_elasticsearch_and_init()
    #init_elasticsearch_future = connect_and_init_elasticsearch()
    #asyncio.gather(init_mongo_future, init_elasticsearch_future)
    #connect_and_init_memcached()


async def shutdown():
    await close_mongo_connect()
    await close_elasticsearch_connect()
    #close_memcached_connect()
