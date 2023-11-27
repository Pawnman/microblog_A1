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

    '''async def create(self, student: UpdateStudentModel) -> str:
        insert_result = await self._db_collection.insert_one(dict(student))
        return str(insert_result.inserted_id)
'''
    async def get_all(self) -> list[UserAccount]:
        db_users = []
        async for user in self._db_collection.find():
            db_users.append(map_users_id_with_name(user))
        return db_users

    async def post_user_account(self, data: UserAccount) -> str:
        insert_result = await self._db_collection.insert_one(dict(data))
        return str(insert_result.inserted_id)

    @staticmethod
    def get_instance(db_collection: AsyncIOMotorCollection = Depends(get_db_users_collection)):
        return Users(db_collection)
'''
    async def get_by_id(self, student_id: str) -> Student | None:
        print(f'Get student {student_id} from mongo')
        db_student = await self._db_collection.find_one(get_filter(student_id))
        return map_student(db_student)

    async def update(self, student_id: str, student: UpdateStudentModel) -> Student | None:
        db_student = await self._db_collection.find_one_and_replace(get_filter(student_id), dict(student))
        return map_student(db_student)

    async def delete(self, student_id: str) -> Student | None:
        db_student = await self._db_collection.find_one_and_delete(get_filter(student_id))
        return map_student(db_student)


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

    @staticmethod
    def get_instance(db_collection: AsyncIOMotorCollection = Depends(get_db_messsages_collection)):
        return Messages(db_collection)