from typing import Any
from bson import ObjectId
from Classes import UserAccount, Message

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