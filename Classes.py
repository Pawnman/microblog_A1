from pydantic import BaseModel
import datetime

class UserAccount(BaseModel):
    name: str = ""
    email: str = ""
    password: str = ""
    created_at: datetime.datetime = None
    followers: list = []
    following: list = []
    messages: list = []
    active: bool = True

class Message(BaseModel):
    user_id: str = None
    message: str = ""
    created_at: datetime.datetime = None
    
    

    
