from typing import Any
from bson import ObjectId
from models.message import Tweet, TweetUpdate
from models.user import User, UserUpdate

def map_users_id_with_name(user: Any) -> User | None:
    if user is None:
        return None
    print(str(user['_id']))
    return User(id=str(user['_id']), name=user['name'], age=user['age'],
                        email=user['email'], created_at=user['created_at'],
                        followers=user['followers'], following=user['following'],
                        active=user['active'])

def user_struct_update(user: User, user_update: UserUpdate) -> User:
    user.name = user_update.name
    return user


def map_message_id(message: Any) -> Tweet | None:
    if message is None:
        return None
    print(str(message['_id']))
    return Tweet(id=str(message['_id']),
                    user_id=message['user_id'], text=message['text'],
                    created_date=message['created_date'],
                    created_time=message['created_time'])

def tweet_struct_update(tweet: Tweet, tweet_update: TweetUpdate) -> Tweet:
    tweet.text = tweet_update.text
    return tweet

def get_filter(id: str) -> dict:
    return {'_id': ObjectId(id)}