import datetime
from pydantic import BaseModel


# Класс поста пользователя с id поста, его содержанием и датой/временем создания
class Tweet(BaseModel):
    user_id: str
    tweet_id: str
    text: str
    created_date: str = str(datetime.datetime.now()).split(' ')[0]
    created_time: str = str(datetime.datetime.now()).split(' ')[1]