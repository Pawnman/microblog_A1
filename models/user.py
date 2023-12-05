import datetime
from pydantic import BaseModel

# Вынести подписчиков в отдельный класс?
class User(BaseModel):
    id: str
    name: str
    age: int
    email: str
    created_at: str = str(datetime.datetime.now()).split(' ')[0]
    followers: list
    following: list = []

class UserUpdate(BaseModel):
    name: str
    email: str
    followers: list = []
    following: list = []
