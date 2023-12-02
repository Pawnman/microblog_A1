from pymongo import MongoClient
from bson import ObjectId
from typing import Optional
from models.Classes import UserAccount, Message
import datetime

CONNECTION_STRING = "mongodb://localhost:27017"
client = MongoClient(CONNECTION_STRING)
db = client.microblog

def get_collection(collection_name: str) -> list[Optional[dict]]:
    col = list(db[collection_name].find({}, {'_id': 0}))
    return col

def get_document(id: str, collection_name: str) -> Optional[dict]:  
    doc = db[collection_name].find_one({"_id": ObjectId(id)}, {'_id': 0})
    return doc

def post_UserAccount(data: UserAccount):
    db["UserAccount"].insert_one(dict(data))

def post_Message(data: Message):
    db["Messages"].insert_one(dict(data))
   
def update_UserAccount(id: str, data: UserAccount):
    db["UserAccount"].find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(data)})
 
def update_Message(id: str, data: Message):
    db["Messages"].find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(data)})

def delete_document(id:str, collection_name: str):
    db[collection_name].find_one_and_delete({"_id":ObjectId(id)})

def follow(id1:str, id2: str):
    user = get_document(id1, "UserAccount")
    other = get_document(id2, "UserAccount")
    if not (user and other):
        raise Exception("One or both users do not exist.")
    if not user["active"] or not other["active"]:
        raise Exception("Inactive user")
    if id2 in user["following"]:
        raise Exception("You are already following this user.")
    else:
        user["following"].append(id2)
        other["followers"].append(id1)
        update_UserAccount(id1, UserAccount(**user))
        update_UserAccount(id2, UserAccount(**other))

def unfollow(id:str, id2: str):
    user = get_document(id, "UserAccount")
    other = get_document(id2, "UserAccount")
    if not (user and other):
        raise Exception("One or both users do not exist.")
    if not user["active"] or not other["active"]:
        raise Exception("Inactive user")
    if id2 not in user["following"]:
        raise Exception("You are not currently following that user.")
    else:
        user["following"].remove(id2)
        other["followers"].remove(id)
        update_UserAccount(id, UserAccount(**user))
        update_UserAccount(id2, UserAccount(**other))

def tweet(id: str, text: str):
    user = get_document(id, "UserAccount")
    if not user["active"]:
        raise Exception("User is inactive")
    message = {
            "user_id": id,
            "message": text,
            "created_at": datetime.datetime.now()}
    if not user:
        raise Exception("That user does not exist.")
    else:
        _id = db["Messages"].insert_one(message)
        user["messages"].append(_id.inserted_id)
        update_UserAccount(id, UserAccount(**user))
        
def delete_tweet(id: str):
    message = get_document(id, "Messages")
    if not message:
        raise Exception("That tweet does not exist.")
    else:
        _id = message["user_id"]
        user = get_document(_id, "UserAccount")
        user["messages"].remove(id)
        update_UserAccount(_id, UserAccount(**user))
        delete_document(id, "Messages")
    
def ban(id: str, state: bool = False):
    user = get_document(id, "UserAccount")
    if user["active"] != state:
        user["active"] = state
        update_UserAccount(id, UserAccount(**user)) 
    else:
        raise Exception("User is already inactive")

