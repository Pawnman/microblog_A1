import datetime
from pydantic import BaseModel

class User(BaseModel):
    #id: str #delete
    name: str = ""
    age: int = 0
    email: str = ""
    created_at: str = str(datetime.datetime.now()).split(' ')[0]
    followers: list = []
    following: list = []
    active: bool = True

class UserUpdate(BaseModel): #delete ????
    name: str = ""
    #email: str = ""
    followers: list = []
    following: list = []


class UpdateUserName(BaseModel):
    name: str = ""

class UpdateFollowers(BaseModel):
    followers: list = []
    following: list = []
