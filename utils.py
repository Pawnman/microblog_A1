from typing import Any
from bson import ObjectId
from models.Classes import UserAccount, Message
from db import connect_and_init_mongo, close_mongo_connect
from utils.elasticsearch_utils import connect_elasticsearch_and_init, close_elasticsearch_connect

## TODO объединить

def map_users_id_with_name(user: Any) -> UserAccount | None:
    if user is None:
        return None
    print(str(user['_id']))
    return UserAccount(id=str(user['_id']), name=user['name'],
                        email=user['email'], active=user['active'])

def map_message_id(message: Any) -> Message | None:
    if message is None:
        return None
    print(str(message['_id']))
    return Message(id=str(message['_id']), 
                    user_id=message['user_id'], message=message['message'])



def get_filter(id: str) -> dict:
    return {'_id': ObjectId(id)}

# Запуск MongoDB и ElasticSearch при запуске приложения
async def handle_startup():
    await connect_and_init_mongo()
    await connect_elasticsearch_and_init()

# Закрытие MongoDB и ElasticSearch при закрытии приложения
async def handle_shutdown():
    await close_mongo_connect()
    await close_elasticsearch_connect()