import datetime
from pydantic import BaseModel


# Пост пользователя
class Tweet(BaseModel):
    user_id: str = ""
    #tweet_id: str
    text: str = ""
    created_date: str = str(datetime.datetime.now()).split(' ')[0]
<<<<<<< HEAD
    created_time: str = str(datetime.datetime.now())
=======
    created_time: str = str(datetime.datetime.now().replace(microsecond=0)).split(' ')[1]
>>>>>>> main
