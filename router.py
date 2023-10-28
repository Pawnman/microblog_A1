from fastapi import APIRouter
from Classes import UserAccount
from bson import ObjectId
import json
from pymongo import MongoClient
import asyncio

CONNECTION_STRING = "mongodb://localhost:27017"
client = MongoClient(CONNECTION_STRING)
db = client.microblog
router = APIRouter()
 
 
@router.get("/")
async def get_collection(collection_name, id: str = "all"):
    if id  == "all": 
        cursor = db[collection_name].find({id}, {'_id': 0}) 
        return list(cursor)
    else:
        doc = db[collection_name].find_one({"_id": ObjectId(id)}, {'_id': 0})
        if doc:
            return doc
        else:
            return None        
        
@router.post("/")
async def post_document(data, collection_name):
    db[collection_name].insert_one(json.loads(data))
   
@router.put("/{id}")
async def update_document(id: str, data, collection_name):
    db[collection_name].find_one_and_update({"_id": ObjectId(id)}, {"$set": json.loads(data)})
 
@router.delete("/{id}")
async def delete_document(id:str, collection_name):
    db[collection_name].find_one_and_delete({"_id":ObjectId(id)})
