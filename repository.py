from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorCollection

from db import get_db_users_collection, get_db_messsages_collection
#from student import Student, UpdateStudentModel
from Classes import UserAccount, Message
from utils import *

## TODO интерфейсный класс

class Users:
    _db_collection: AsyncIOMotorCollection

    def __init__(self, db_collection: AsyncIOMotorCollection):
        self._db_collection = db_collection

    async def get_all(self) -> list[UserAccount]:
        db_users = []
        async for user in self._db_collection.find():
            db_users.append(map_users_id_with_name(user))
        return db_users

    async def get_by_id(self, user_id: str) -> UserAccount | None:
        print(f'Get user account {user_id} from mongo')
        db_user = await self._db_collection.find_one(get_filter(user_id))
        return map_users_id_with_name(db_user)
    
    async def post_user_account(self, data: UserAccount) -> str:
        insert_result = await self._db_collection.insert_one(dict(data))
        return str(insert_result.inserted_id)
    
    async def delete(self, id: str) -> UserAccount | None:
        db_user = await self._db_collection.find_one_and_delete(get_filter(id))
        return map_users_id_with_name(db_user)

    async def update(self, id: str, data: UserAccount):
        db_user = await self._db_collection.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(data)})
        return map_users_id_with_name(db_user)

    @staticmethod
    def get_instance(db_collection: AsyncIOMotorCollection = Depends(get_db_users_collection)):
        return Users(db_collection)


'''
def update_UserAccount(id: str, data: UserAccount):
    db["UserAccount"].find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(data)})
 
def update_Message(id: str, data: Message):
    db["Messages"].find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(data)})
'''


class Messages:
    _db_collection: AsyncIOMotorCollection

    def __init__(self, db_collection: AsyncIOMotorCollection):
        self._db_collection = db_collection

    async def get_all(self) -> list[Message]:
        db_messages = []
        async for message in self._db_collection.find():
            db_messages.append(map_message_id(message))
        return db_messages

    async def post_message(self, data: Message) -> str:
        insert_result = await self._db_collection.insert_one(dict(data))
        return str(insert_result.inserted_id)

    async def get_by_id(self, message_id: str) -> UserAccount | None:
        print(f'Get message {message_id} from mongo')
        db_message = await self._db_collection.find_one(get_filter(message_id))
        return map_message_id(db_message)

    async def update(self, id: str, data: Message):
        db_message = await self._db_collection.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(data)})
        return map_message_id(db_message)

    @staticmethod
    def get_instance(db_collection: AsyncIOMotorCollection = Depends(get_db_messsages_collection)):
        return Messages(db_collection)