from pymongo import MongoClient
from bson import ObjectId
from typing import Optional, List
from Classes import UserAccount, Message

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
