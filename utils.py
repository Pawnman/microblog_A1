from typing import Any
from bson import ObjectId
from models.message import Tweet
from models.user import User
from local_utils.elasticsearch_utils import connect_and_init_elasticsearch, close_connection_elasticsearch

## TODO объединить

def map_users_id_with_name(user: Any) -> User | None:
    if user is None:
        return None
    print(str(user['_id']))
    return User(id=str(user['_id']), name=user['name'],
                        email=user['email'], active=user['active'])

def map_message_id(message: Any) -> Tweet | None:
    if message is None:
        return None
    print(str(message['_id']))
    return Tweet(id=str(message['_id']),
                    user_id=message['user_id'], message=message['message'])



def get_filter(id: str) -> dict:
    return {'_id': ObjectId(id)}

#delete
# Запуск MongoDB и ElasticSearch при запуске приложения
async def handle_startup():
    await connect_and_init_mongo()
    await connect_and_init_elasticsearch()

#delete
# Закрытие MongoDB и ElasticSearch при закрытии приложения
async def handle_shutdown():
    await close_mongo_connect()
    await close_connection_elasticsearch()