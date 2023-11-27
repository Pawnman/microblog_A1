from typing import Any
from bson import ObjectId
from Classes import UserAccount, Message

## TODO объединить

def map_users_id_with_name(user: Any) -> UserAccount | None:
    if user is None:
        return None
    return UserAccount(id=str(user['_id']), name=user['name'])

def map_message_id(message: Any) -> Message | None:
    if message is None:
        return None
    return Message(id=str(message['_id']), message=message['message'])



def get_filter(id: str) -> dict:
    return {'_id': ObjectId(id)}