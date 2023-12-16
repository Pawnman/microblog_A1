import datetime
from pydantic import BaseModel


# Пост пользователя
class Tweet(BaseModel):
    user_id: str = ""
    #tweet_id: str
    text: str = ""
    created_date: str = str(datetime.datetime.now()).split(' ')[0]
    created_time: str = str(datetime.datetime.now()).split(' ')[1]