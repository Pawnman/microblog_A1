from typing import Any

from bson import ObjectId
from fastapi import APIRouter, status, Depends
from starlette.responses import Response
from models.user import User
from models.message import Tweet

#from cache.memcached_utils import get_memcached_client
from repository import Users, Messages
from local_utils.searchdb_repo import *
from local_utils.searchdb_repo import UserSearchRepository, MessageSearchRepository

router = APIRouter()

@router.get("/get_all_users")
async def get_all_users(users: Users = Depends(Users.get_instance)) -> list[User]:
    return await users.get_all()


@router.get("/{id}_get_user_account", response_model=User)
async def get_by_id(id: str,
                    users: Users = Depends(Users.get_instance)) -> Any:
    if not ObjectId.is_valid(id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    #student = memcached_client.get(id)
    #if student is not None:
        #return student
    user = await users.get_by_id(id)
    if user is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    #memcached_client.add(id, student)
    return user

# Поиск пользователя по его имени
@router.get("/users", response_model=list[User])
async def find_user_by_name(name: str,
                            search_db: MessageSearchRepository = Depends(MessageSearchRepository.get_instance)):
    return await search_db.get_by_name(name)

@router.get("/get_all_messages")
async def get_all_messages(messages: Messages = Depends(Messages.get_instance)) -> list[Tweet]:
    return await messages.get_all()

@router.get("/{id}_get_message", response_model=Tweet)
async def get_by_id(id: str,
                    messages: Messages = Depends(Messages.get_instance)) -> Any:
    if not ObjectId.is_valid(id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    #messages = memcached_client.get(id)
    #if messages is not None:
        #return student
    message = await messages.get_by_id(id)
    if message is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    #memcached_client.add(id, message)
    return message

@router.post("/post_UserAccount")
async def post_user_account(data: User,
                            users: Users = Depends(Users.get_instance),
                            messages_elsearch: MessageSearchRepository = Depends(MessageSearchRepository.get_instance) #WTF???
                            ) -> str:
    user_id = await users.post_user_account(data)
    await messages_elsearch.create_user(user_id, data)
    #await local_utils.searchdb_repo.create_user(user_id, data)
    return user_id

@router.post("/post_Message")
async def post_message(data: Tweet,
                        messages: Messages = Depends(Messages.get_instance),
                        messages_elsearch: MessageSearchRepository = Depends(MessageSearchRepository.get_instance)
                        ) -> str:
    message_id = await messages.post_message(data)
    #await local_utils.searchdb_repo.create_message(message_id, data)
    await messages_elsearch.create_message(message_id, data)
    return message_id

@router.delete("/{id}")
async def remove_user(id: str, users: Users = Depends(Users.get_instance)) -> Response:
    if not ObjectId.is_valid(id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    user = await users.delete(id)
    if user is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    #await local_utils.searchdb_repo.delete_user(id)
    await delete_user(id)
    return Response()

@router.put("/{id}_user", response_model=User)
async def update_user_account(id: str, data: User,
                              users: Users = Depends(Users.get_instance)) -> Any:
    if not ObjectId.is_valid(id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    user = await users.update(id, data)
    if user is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return user


@router.put("/{id}_message", response_model=Tweet)
async def update_message(id: str, data: Tweet,
                         messages: Messages = Depends(Messages.get_instance)) -> Any:
    if not ObjectId.is_valid(id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    message = await messages.update(id, data)
    if message is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return message

# Поиск твита конкретного пользователя
@router.get("/users/{user_id}/tweets/search", response_model=list[Tweet])
async def find_tweet(pattern: str, user_id: str,
                     search_db: MessageSearchRepository = Depends(MessageSearchRepository.get_instance)):
    if not ObjectId.is_valid(user_id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    return await search_db.find_tweet(user_id, pattern)

# Посик твитов конкретного пользователя за последний час и день
# Тут нужно быть аккуратным с директориями
@router.get("/users/{user_id}/tweets/search", response_model=list[Tweet])
async def find_tweet_hour(user_id: str,
                          search_db: MessageSearchRepository = Depends(MessageSearchRepository.get_instance)):
    if not ObjectId.is_valid(user_id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    return await search_db.search_last_hour(user_id)

@router.get("/users/{user_id}/tweets/search", response_model=list[Tweet])
async def find_tweet_day(user_id: str,
                         search_db: MessageSearchRepository = Depends(MessageSearchRepository.get_instance)):
    if not ObjectId.is_valid(user_id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    return await search_db.search_last_day(user_id)



'''
@router.put("/{id1}_{id2}_Follow")
async def follow(id1: str, id2: str):
    q.follow(id1, id2)

@router.put("/{id1}_{id2}_Unfollow")
async def unfollow(id1:str, id2: str):
    q.unfollow(id1, id2)
    
@router.put("/{id}_Ban")
async def ban(id: str, state: bool = False):
    q.ban(id, state) 


@router.delete("/{id}_delete_tweet")
async def delete_tweet(id: str, messages: Messages = Depends(Messages.get_instance)) -> Response:
    q.delete_tweet(id)

'''

''''
@router.get("/get_all_messages")
async def get_all_users(repository: Repository = Depends(Repository.get_instance)) -> list[UserAccount]:
    return await repository.get_all()
    '''


'''from fastapi import APIRouter
from typing import Optional
from Classes import UserAccount, Message
#import queries as q

router = APIRouter()


@router.get("/get_collection")
async def get_collection(collection_name: str) -> list[Optional[dict]]:
    return q.get_collection(collection_name)

@router.get("/{id}_get_document")
async def get_document(id: str, collection_name: str) -> Optional[dict]:
    return q.get_document(id, collection_name)
        
@router.post("/post_UserAccount")
async def post_UserAccount(data: UserAccount):
    q.post_UserAccount(data)

@router.post("/post_Message")
async def post_Message(data: Message):
    q.post_Message(data)
   
@router.post("/{id}_{text}_tweet")
async def tweet(id: str,text: str):
    q.tweet(id, text)

@router.put("/{id}_Update_account")
async def update_UserAccount(id: str, data: UserAccount):
    q.update_UserAccount(id, data)
 
@router.put("/{id}_Update_message")
async def update_Message(id: str, data: Message):
    q.update_Message(id, data)

@router.put("/{id1}_{id2}_Follow")
async def follow(id1: str, id2: str):
    q.follow(id1, id2)

@router.put("/{id1}_{id2}_Unfollow")
async def unfollow(id1:str, id2: str):
    q.unfollow(id1, id2)
    
@router.put("/{id}_Ban")
async def ban(id: str, state: bool = False):
    q.ban(id, state) 
    
@router.delete("/{id}")
async def delete_document(id:str, collection_name: str):
    q.delete_document(id, collection_name)

@router.delete("/{id}_delete_tweet")
async def delete_tweet(id: str):
    q.delete_tweet(id)
'''
