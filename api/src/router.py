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

'''
post user 2
user.update: update model use
following / un
ban
("/{id}_{text}_tweet")
("/{id}_Update_account")
 
"/{id}_Update_message")
'''




@router.get("/get_all_users")
async def get_all_users(users: Users = Depends(Users.get_instance)) -> list[User]:
    return await users.get_all()


@router.get("/get_user_account_by_id/{id}", response_model=User)
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

@router.get("/get_users_by_name", response_model=list[User])
async def find_user_by_name(name: str,
                            search_db: MessageSearchRepository = 
                                Depends(MessageSearchRepository.get_instance)):
    user_list = await search_db.get_by_name(name)
    return user_list

 #у каждого пользователя уникальный email, но можно искать пользователей с похожими email
 #идея: регулярка для поиска по доменам например (теоритически для предотвращения регистрации на
 # одну почту, но с разными доменами. Хотя это скорее всего не по поиску делается)
 #если поиск точный, то недопуск регистрации на 1 имэйл
@router.get("/get_user_by_email", response_model=list[User])
async def get_user_by_email(email: str,
                            search_db: MessageSearchRepository = 
                                Depends(MessageSearchRepository.get_instance)):
    user_list = await search_db.get_by_email(email)
    if user == []:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    print(f'user: {user}')
    return user

@router.get("/get_all_tweets")
async def get_all_tweets(messages: Messages = Depends(Messages.get_instance)) -> list[Tweet]:
    return await messages.get_all()

@router.get("/get_tweet_by_id/{id}", response_model=Tweet)
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

@router.get("/get_tweets_by_pattern/{user_id}", response_model=list[Tweet])
async def find_tweet(pattern: str, user_id: str,
                    search_db: MessageSearchRepository =
                        Depends(MessageSearchRepository.get_instance)):
    if not ObjectId.is_valid(user_id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    return await search_db.find_tweet(user_id, pattern)

# Поиск твитов конкретного пользователя за последний час и день
@router.get("/get_tweet_for_last_hour/{user_id}", response_model=list[Tweet])
async def find_tweet_hour(user_id: str,
                        search_db: MessageSearchRepository =
                            Depends(MessageSearchRepository.get_instance)):
    if not ObjectId.is_valid(user_id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    return await search_db.search_tweet_last_hour(user_id)

@router.get("/get_tweet_for_last_day/{user_id}", response_model=list[Tweet])
async def find_tweet_day(user_id: str,
                        search_db: MessageSearchRepository =
                            Depends(MessageSearchRepository.get_instance)):
    if not ObjectId.is_valid(user_id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    return await search_db.search_tweet_last_day(user_id)


@router.post("/post_user_account")
async def post_user_account(data: User,
                            users: Users = Depends(Users.get_instance),
                            search_db: MessageSearchRepository =
                                Depends(MessageSearchRepository.get_instance)
                            ) -> str:
    emails = await search_db.get_by_email(data.email)
    print(emails)
    if (emails != []):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
                            
    user_id = await users.post_user_account(data)
    await search_db.create_user(user_id, data)
    return user_id

@router.post("/post_tweet")#2
async def post_message(data: Tweet,
                        messages: Messages = Depends(Messages.get_instance),
                        search_db: MessageSearchRepository =
                            Depends(MessageSearchRepository.get_instance)
                        ) -> str:
    message_id = await messages.post_message(data)
    await search_db.create_message(message_id, data)
    return message_id

@router.delete("/delete_user_by_id/{user_id}")
async def remove_user(user_id: str, users: Users = Depends(Users.get_instance),
                         search_db: MessageSearchRepository =
                                Depends(MessageSearchRepository.get_instance)) -> Response:
    if not ObjectId.is_valid(user_id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    user = await users.delete(user_id)
    if user is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    await search_db.delete_user(user_id)
    return Response()

@router.delete("/delete_tweet_by_id/{message_id}")
async def remove_user(message_id: str, 
                            messages: Messages = Depends(Messages.get_instance),
                            search_db: MessageSearchRepository =
                                Depends(MessageSearchRepository.get_instance)) -> Response:
    if not ObjectId.is_valid(message_id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    user = await users.delete(message_id)
    if user is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    await search_db.delete_message(message_id)
    return Response()

@router.put("/update_user_account/{id}", response_model=User) #!!!!!!!! add elastic add UserUpdate
async def update_user_account(id: str, data: User,
                            users: Users = Depends(Users.get_instance),
                            search_db: MessageSearchRepository =
                                Depends(MessageSearchRepository.get_instance)) -> Any:
    if not ObjectId.is_valid(id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    user = await users.update(id, data)
    if user is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return user

''''
#воможно позже, пока без обновления соообщений
@router.put("/update_tweet{id}", response_model=Tweet)
async def update_tweet(id: str, data: Tweet,
                        messages: Messages = Depends(Messages.get_instance),
                        search_db: MessageSearchRepository =
                                Depends(MessageSearchRepository.get_instance)) -> Any:
    if not ObjectId.is_valid(id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    message = await messages.update(id, data)
    if message is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return message
'''
#id1 подписывается на id2
@router.put("/follow/{id1}/to/{id2}")
async def follow(id1: str, id2: str, users: Users = Depends(Users.get_instance),
                search_db: MessageSearchRepository =
                                Depends(MessageSearchRepository.get_instance)) -> Response:
    if id1 == id2:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    if not ObjectId.is_valid(id1) and  not ObjectId.is_valid(id2):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)

    user1 = await users.get_by_id(id1)
    user2 = await users.get_by_id(id2)
    if user1 is None or user2 is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    sucsess = await users.follow(id1, user1, id2, user2)
    if sucsess is False:
        return Response(status_code=status.HTTP_520_UNKNOWN_ERROR)


    #elastic
    return Response()

#id1 отписывается от id2
@router.put("/unfollow/{id1}/from/{id2}")
async def unfollow(id1: str, id2: str, users: Users = Depends(Users.get_instance),
                search_db: MessageSearchRepository =
                                Depends(MessageSearchRepository.get_instance)) -> Response:
    if not ObjectId.is_valid(id1) and  not ObjectId.is_valid(id2):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    user1 = await users.get_by_id(id1)
    user2 = await users.get_by_id(id2)
    if user1 is None or user2 is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    sucsess = await users.unfollow(id1, user1, id2, user2)
    if sucsess is False:
        return Response(status_code=status.HTTP_520_UNKNOWN_ERROR)


    #elastic
    return Response()
    
    
#@router.put("/ban/{user_id}")
#async def ban(id: str, state: bool = False) -> Response:
    


'''from fastapi import APIRouter
from typing import Optional
from Classes import UserAccount, Message
#import queries as q

router = APIRouter()

@router.get("/get_all_messages")
async def get_all_users(repository: Repository = Depends(Repository.get_instance)) -> list[UserAccount]:
    return await repository.get_all()

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
