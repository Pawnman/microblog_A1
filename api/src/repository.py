from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorCollection

from db import get_db_users_collection, get_db_messsages_collection
from models.user import User, UpdateFollowers
#from student import Student, UpdateStudentModel
from utils import *

## TODO интерфейсный класс

class Users:
    _db_collection: AsyncIOMotorCollection

    def __init__(self, db_collection: AsyncIOMotorCollection):
        self._db_collection = db_collection

    async def get_all(self) -> list[User]:
        db_users = []
        async for user in self._db_collection.find():
            db_users.append(map_users_id_with_name(user))
        return db_users

    async def get_by_id(self, user_id: str) -> User | None:
        print(f'Get user account {user_id} from mongo')
        db_user = await self._db_collection.find_one(get_filter(user_id))
        return map_users_id_with_name(db_user)
    
    async def post_user_account(self, data: User) -> str:
        insert_result = await self._db_collection.insert_one(dict(data))
        return str(insert_result.inserted_id)
    
    async def delete(self, id: str) -> User | None:
        db_user = await self._db_collection.find_one_and_delete(get_filter(id))
        return map_users_id_with_name(db_user)

    async def update(self, user_id: str, user: User) -> User | None: 
        db_user = await self._db_collection.find_one_and_replace(get_filter(user_id), dict(user))
        return map_users_id_with_name(db_user)

    async def follow(self, user_id: str, user: User, following_user_id: str, following_user: User) ->  bool:
        print(f'following_user id: {following_user_id}')
        print(f'user id: {user_id}')
        print(f'user following before.. {user.following}')
        print(f'user followers before.. {user.followers}')
        print(f'following_user following before.. {following_user.following}')
        print(f'following_user followers before.. {following_user.followers}')
        if (user.following.find(following_user_id)):
            return False
        user.following.append(following_user_id)
        following_user.followers.append(user_id)
        
        update_user = await self.update(user_id, user)
        update_following_user = await self.update(following_user_id, following_user)

        print(f'user following after.. {user.following}')
        print(f'user followers after.. {user.followers}')
        print(f'following_user following after.. {following_user.following}')
        print(f'following_user followers after.. {following_user.followers}')
        
        update_user = await self.update(user_id, user)
        update_following_user = await self.update(following_user_id, following_user)
        if update_user is None or update_following_user is None:
            return False
        return True

    async def unfollow(self, user_id: str, user: User, following_user_id: str, following_user: User) ->  bool:
        print(f'following_user id: {following_user_id}')
        print(f'user id: {user_id}')
        user.following.remove(following_user_id)
        following_user.followers.remove(user_id)

        update_user = await self.update(user_id, user)
        update_following_user = await self.update(following_user_id, following_user)
        if update_user is None or update_following_user is None:
            return False
        return True

    async def ban(self, user_id: str, user: User, state: bool) -> User | None:
        user.active = state
        return await self.update(user_id, user)
        
    @staticmethod
    def get_instance(db_collection: AsyncIOMotorCollection = Depends(get_db_users_collection)):
        return Users(db_collection)
    

class Messages:
    _db_collection: AsyncIOMotorCollection

    def __init__(self, db_collection: AsyncIOMotorCollection):
        self._db_collection = db_collection

    async def get_all(self) -> list[Tweet]:
        db_messages = []
        async for message in self._db_collection.find():
            db_messages.append(map_message_id(message))
        return db_messages

    async def post_message(self, data: Tweet) -> str:
        insert_result = await self._db_collection.insert_one(dict(data))
        return str(insert_result.inserted_id)

    async def get_by_id(self, message_id: str) -> User | None:
        print(f'Get message {message_id} from mongo')
        db_message = await self._db_collection.find_one(get_filter(message_id))
        return map_message_id(db_message)

    async def update(self, id: str, data: Tweet):
        db_message = await self._db_collection.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(data)})
        return map_message_id(db_message)

    async def delete(self, id: str) -> Tweet | None:
        db_message = await self._db_collection.find_one_and_delete(get_filter(id))
        return map_message_id(db_message)

    @staticmethod
    def get_instance(db_collection: AsyncIOMotorCollection = Depends(get_db_messsages_collection)):
        return Messages(db_collection)