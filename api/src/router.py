from typing import Any

from bson import ObjectId
from fastapi import APIRouter, status, Depends
from starlette.responses import Response
from models.user import User, UserUpdate
from models.message import Tweet, TweetUpdate

from pymemcache import HashClient
from memcache import get_memcached_client
from repository import Users, Messages
from search_engine.search_repository import UserSearchRepository, MessageSearchRepository
from utils import tweet_struct_update, user_struct_update

router = APIRouter()


@router.get("/get_all_users")
async def get_all_users(users: Users = Depends(Users.get_instance)) -> list[User]:
    return await users.get_all()

@router.get("/get_user_account_by_id/{id}", response_model=User)
async def get_by_id(id: str,
                    users: Users = Depends(Users.get_instance),
                    memcached_client: HashClient = Depends(get_memcached_client)) -> Any:
    if not ObjectId.is_valid(id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    
    print(memcached_client)
    user = memcached_client.get(id)
    if user is not None:
        print('using cached user data')
        return user
    
    user = await users.get_by_id(id)
    if user is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    memcached_client.add(id, user)
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
    if user_list == []:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    #print(f'user: {user_list[0]}')
    return user_list

@router.get("/get_all_tweets")
async def get_all_tweets(messages: Messages = Depends(Messages.get_instance)) -> list[Tweet]:
    return await messages.get_all()

@router.get("/get_tweet_by_id/{id}", response_model=Tweet)
async def get_by_id(id: str,
                    messages: Messages = Depends(Messages.get_instance),
                    memcached_client: HashClient = Depends(get_memcached_client)) -> Any:
    if not ObjectId.is_valid(id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    
    message_cached = memcached_client.get(id)
    if message_cached is not None:
        print('Using cached message data')
        return message_cached

    message = await messages.get_by_id(id)
    if message is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    memcached_client.add(id, message)
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
  #  if (emails != []):
  #      return Response(status_code=status.HTTP_400_BAD_REQUEST)
                            
    user_id = await users.post_user_account(data)
    await search_db.create_user(user_id, data)
    return user_id

@router.post("/post_tweet")
async def post_message(data: Tweet,
                        messages: Messages = Depends(Messages.get_instance),
                        users: Users = Depends(Users.get_instance),
                        search_db: MessageSearchRepository =
                            Depends(MessageSearchRepository.get_instance)
                        ) -> str:
    
    if not ObjectId.is_valid(data.user_id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    user = await users.get_by_id(data.user_id)
    if user is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    if user.active == False:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)

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
async def remove_message(message_id: str, 
                            messages: Messages = Depends(Messages.get_instance),
                            search_db: MessageSearchRepository =
                                Depends(MessageSearchRepository.get_instance)) -> Response:
    if not ObjectId.is_valid(message_id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)

    message_id_result = await messages.delete(message_id)
    if message_id_result is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    await search_db.delete_message(message_id)
    return Response()

@router.put("/update_user_account/{id}", response_model=User)
async def update_user_account(id: str, data: UserUpdate,
                            users: Users = Depends(Users.get_instance),
                            search_db: MessageSearchRepository =
                                Depends(MessageSearchRepository.get_instance)) -> Any:
    if not ObjectId.is_valid(id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)

    old_user_data = await users.get_by_id(id)
    new_data: User = user_struct_update(old_user_data, data)
    user = await users.update(id, new_data)
    if user is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    await search_db.update_user(id, new_data)
    return user

@router.put("/update_tweet/{id}", response_model=TweetUpdate)
async def update_tweet(id: str, data: TweetUpdate,
                        messages: Messages = Depends(Messages.get_instance),
                        search_db: MessageSearchRepository =
                                Depends(MessageSearchRepository.get_instance)) -> Any:
    if not ObjectId.is_valid(id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)

    old_message = await messages.get_by_id(id)
    new_data: Tweet = tweet_struct_update(old_message, data)
    message = await messages.update(id, new_data)
    if message is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    await search_db.update_message(id, new_data)
    return message


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
    return Response()
    
    
@router.put("/ban/{user_id}")
async def ban(user_id: str, state: bool = False,
                            users: Users = Depends(Users.get_instance),
                            search_db: MessageSearchRepository =
                                Depends(MessageSearchRepository.get_instance)) -> Response:
    if not ObjectId.is_valid(user_id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    user = await users.get_by_id(user_id)
    if user is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    update_user = await users.ban(user_id, user, state)
    if update_user is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return Response()
