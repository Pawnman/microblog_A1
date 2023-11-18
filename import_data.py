import xml.etree.ElementTree as ET
import secrets
import pymongo
from pymongo import MongoClient
import Classes
from pydantic import BaseModel

CONNECTION_STRING = "mongodb://localhost:27017"
client = MongoClient(CONNECTION_STRING)
db = client["microblog"]


""" UserAccount = {
    "AccountId" : "",
    "name" : "",
    "email" : "",
    "password" : "",
    "created_at" : "",
    "followers" : "0",
    "following" : "0",
    "'active" : "0"
}

Message  = {
    "user_id" :  "",
    "message" :  "",
    "created_at" : ""
} """

def email_generator():
    return f"{secrets.token_hex(8)}@gmail.com"

def password_generator():
    return f"{secrets.token_hex(3)}"

collection = db["UserAccount"]
users_id = {}

for event, elem in ET.iterparse("data\\xml\\Users.xml"):
    rec = elem.attrib
    user_account = Classes.UserAccount()
    try:
        #user_account.account_id  = rec["AccountId"]
        account_id  = rec["Id"]
        user_account.name =  rec["DisplayName"]
        user_account.email = email_generator()
        user_account.password = password_generator()
        user_account.created_at = rec["CreationDate"]
        insert_result = collection.insert_one(dict(user_account))
        users_id[account_id] = str(insert_result.inserted_id)
    except KeyError:
        print("Key from Users Not Found.")
    '''
    UserAccount["AccountId"]  = rec["AccountId"]
    UserAccount["name"] =  rec["DisplayName"]
    UserAccount["email"] = email_generator()
    UserAccount["password"] = password_generator()
    UserAccount["created_at"] = rec["CreationDate"]
    '''



collection_messages = db["Messages"]

for event, elem in ET.iterparse("data\\xml\\Posts.xml"):
    rec = elem.attrib
    message = Classes.Message()
    try:
        if rec["PostTypeId"] == '1':
            #message.user_id = rec["OwnerUserId"]
            account_id = rec["OwnerUserId"]
            
            message.user_id = users_id[account_id]
            message.message = rec["Body"]
            message.created_at = rec["CreationDate"]
            collection_messages.insert_one(dict(message))
    except KeyError:
        print("Key from Posts Not Found.")
        '''
        Message["user_id"] = rec["OwnerUserId"]
        Message["message"] = rec["Body"]
        Message["created_at"] = rec["CreationDate"]
        '''
        
