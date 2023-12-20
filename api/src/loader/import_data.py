import xml.etree.ElementTree as ET
import secrets
from pymongo import MongoClient
from models.message import Tweet
from models.user import User
from elasticsearch import Elasticsearch
import os
import sys
import pathlib
from repository import Users, Messages
from local_utils.searchdb_repo import MessageSearchRepository
from db import get_db_users_collection, get_db_messsages_collection
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

sys.path.append(str(pathlib.Path(sys.path[0]).resolve().parent.parent / "data"))
CONNECTION_STRING = "mongodb://localhost:27017"
elasticsearch_uri = "http://localhost:9200"
#USERS_PATH = r"..\..\..\data\xml\Users.xml"
USERS_PATH = r"data\xml\Users_demo.xml"
TWEETS_PATH = r"data\xml\Posts_demo.xml"

client = MongoClient(CONNECTION_STRING)
db = client["microblog"]

elasticsearch_client = Elasticsearch(elasticsearch_uri)
elasticsearch_users_index = "useraccount"
elasticsearch_messages_index = "message"

def email_generator():
    return f"{secrets.token_hex(8)}@gmail.com"

def password_generator():
    return f"{secrets.token_hex(3)}"

def age_generator():
    return secrets.randbelow(70)

users_id = {}


def import_user_accounts():
    collection = db["UserAccount"]
    for event, elem in ET.iterparse(USERS_PATH):
        rec = elem.attrib
        user_account = User()
        try:
            account_id  = rec["Id"]
            user_account.name =  rec["DisplayName"]
            user_account.email = email_generator()
            user_account.age = age_generator()
            #user_account.password = password_generator()
            user_account.created_at = rec["CreationDate"]
        except KeyError:
            print("Key from Users Not Found.")
            continue
        insert_result = collection.insert_one(dict(user_account))
        elasticsearch_client.create(index=elasticsearch_users_index, 
                                    id=str(insert_result.inserted_id), document=dict(user_account))
        users_id[account_id] = str(insert_result.inserted_id)


def import_messages():
    collection = db["Message"]
    for event, elem in ET.iterparse(TWEETS_PATH):
        rec = elem.attrib
        message = Tweet()
        try:
            if rec["PostTypeId"] == '1':
                account_id = rec["OwnerUserId"]
                message.user_id = users_id[account_id]
                message.text = rec["Body"]
                message.created_date = rec["CreationDate"].split("T")[0]
                message.created_time = rec["CreationDate"].split("T")[1]
                insert_result = collection.insert_one(dict(message))
                elasticsearch_client.create(index=elasticsearch_messages_index, 
                                    id=str(insert_result.inserted_id), document=dict(message))
        except KeyError:
            print("Key from Posts Not Found.")
