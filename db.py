import os
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
db_client: AsyncIOMotorClient = None

async def get_db_users_collection() -> AsyncIOMotorCollection:
    mongo_db = os.getenv('MONGO_DB')
    mongo_collection = os.getenv('MONGO_USERS_COLLECTION')
    db = db_client.get_database(mongo_db)
    return db.get_collection(mongo_collection)

async def get_db_messsages_collection() -> AsyncIOMotorCollection:
    mongo_db = os.getenv('MONGO_DB')
    mongo_collection = os.getenv('MONGO_MESSAGES_COLLECTION')
    db = db_client.get_database(mongo_db)
    return db.get_collection(mongo_collection)

async def connect_and_init_mongo():
    global db_client
    mongo_uri = os.getenv('MONGO_URI')
    mongo_db = os.getenv('MONGO_DB')
    mongo_users_collection = os.getenv('MONGO_USERS_COLLECTION')
    mongo_messages_collection = os.getenv('MONGO_MESSAGES_COLLECTION')
    try:
        db_client = AsyncIOMotorClient(mongo_uri)
        await db_client.server_info()
        print(f'Connected to mongo with uri {mongo_uri}')
        print(db_client.list_database_names())
        if mongo_db not in await db_client.list_database_names():
            await db_client.get_database(mongo_db).create_collection(mongo_users_collection)
            await db_client.get_database(mongo_db).create_collection(mongo_messages_collection)
            print(f'Database {mongo_db} created')

    except Exception as ex:
        print(f'Cant connect to mongo: {ex}')


def close_mongo_connect():
    global db_client
    if db_client is None:
        return
    db_client.close()
