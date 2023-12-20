import datetime
from pydantic import BaseModel

class User(BaseModel):
    name: str = ""
    age: int = 0
    email: str = ""
    created_at: str = str(datetime.datetime.now()).split(' ')[0]
    followers: list = []
    following: list = []
    active: bool = True

class UserUpdate(BaseModel):
    name: str = ""


class UpdateFollowers(BaseModel):
    followers: list = []
    following: list = []
