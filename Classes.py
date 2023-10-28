from pydantic import BaseModel
import datetime

class UserAccount(BaseModel):
    id: int = None
    name: str = ""
    email: str = ""
    password: str = ""
    created_at: datetime.datetime = None
    updated_at: datetime.datetime = None
    followers: list = []
    following: list = []
    messages: list = []
    active: bool = True

class Message(BaseModel):
    id: int = None
    user_id: int = None
    message: str = ""
    created_at: datetime.datetime = None
    

    
