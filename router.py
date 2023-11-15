from fastapi import APIRouter
from typing import Optional
from Classes import UserAccount, Message
import queries as q

router = APIRouter()

@router.get("/get_collection")
async def get_collection(collection_name: str) -> list[Optional[dict]]:
    return q.get_collection(collection_name)

@router.get("/{id}_get_document")
async def get_document(id: str, collection_name: str) -> Optional[dict]:
    return q.get_document(id, collection_name)
        
@router.post("/post_UserAccount")
async def post_UserAccount(data: UserAccount):
    q.post_UserAccount(data)

@router.post("/post_Message")
async def post_Message(data: Message):
    q.post_Message(data)
   
@router.post("/{id}_{text}_tweet")
async def tweet(id: str,text: str):
    q.tweet(id, text)

@router.put("/{id}_Update_account")
async def update_UserAccount(id: str, data: UserAccount):
    q.update_UserAccount(id, data)
 
@router.put("/{id}_Update_message")
async def update_Message(id: str, data: Message):
    q.update_Message(id, data)

@router.put("/{id1}_{id2}_Follow")
async def follow(id1: str, id2: str):
    q.follow(id1, id2)

@router.put("/{id1}_{id2}_Unfollow")
async def unfollow(id1:str, id2: str):
    q.unfollow(id1, id2)
    
@router.put("/{id}_Ban")
async def ban(id: str, state: bool = False):
    q.ban(id, state) 
    
@router.delete("/{id}")
async def delete_document(id:str, collection_name: str):
    q.delete_document(id, collection_name)

@router.delete("/{id}_delete_tweet")
async def delete_tweet(id: str):
    q.delete_tweet(id)
