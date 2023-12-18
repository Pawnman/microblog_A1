import xml.etree.ElementTree as ET
import secrets
from pymongo import MongoClient
from models.message import Tweet
from models.user import User
from elasticsearch import AsyncElasticsearch
import os
import sys
import pathlib
from repository import Users, Messages
from local_utils.searchdb_repo import MessageSearchRepository
from db import get_db_users_collection, get_db_messsages_collection
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

sys.path.append(str(pathlib.Path(sys.path[0]).resolve().parent.parent / "data"))
#CONNECTION_STRING = "mongodb://localhost:27017"
#ELASTICSEARCH_URI = os.getenv('ELASTICSEARCH_URI')
#USERS_PATH = r"..\..\..\data\xml\Users.xml"
USERS_PATH = r"data\xml\Users_demo.xml"
TWEETS_PATH = r"..\..\..\data\xml\Posts.xml"

#client = MongoClient(CONNECTION_STRING)
#db = client["microblog"]
#elasticsearch_uri = os.getenv('ELASTICSEARCH_URI')
#elasticsearch_client = AsyncElasticsearch(elasticsearch_uri.split(','))

def email_generator():
    return f"{secrets.token_hex(8)}@gmail.com"

def password_generator():
    return f"{secrets.token_hex(3)}"

users_id = {}

async def import_user_accounts():
    #collection = db["UserAccount"]
    users_mongo_collection = get_db_users_collection()
    #users_mongo_collection = Users.get_instance()
    for event, elem in ET.iterparse(USERS_PATH):
        rec = elem.attrib
        user_account = User()
        try:
            account_id  = rec["Id"]
            user_account.name =  rec["DisplayName"]
            user_account.email = email_generator()
            #user_account.password = password_generator()
            user_account.created_at = rec["CreationDate"]
        except KeyError:
            print("Key from Users Not Found.")
            continue
        #insert_result = await users_mongo_collection.post_user_account(user_account)
        insert_result = await users_mongo_collection.insert_one(dict(user_account))
        #users_id[account_id] = str(insert_result.inserted_id)
        
    print(f'users_ID: {insert_result}')


'''
def import_user_accounts():
    #collection = db["UserAccount"]
    users_mongo_collection = Users.get_db_users_collection()
    for event, elem in ET.iterparse(USERS_PATH):
        rec = elem.attrib
        user_account = User()
        try:
            account_id  = rec["Id"]
            user_account.name =  rec["DisplayName"]
            user_account.email = email_generator()
            #user_account.password = password_generator()
            user_account.created_at = rec["CreationDate"]
        except KeyError:
            print("Key from Users Not Found.")
            continue
        #insert_result = collection.insert_one(dict(user_account))
        users_id[account_id] = str(insert_result.inserted_id)
        '''


def import_messages():
    collection = db["Messages"]
    for event, elem in ET.iterparse(TWEETS_PATH):
        rec = elem.attrib
        message = Tweet()
        try:
            if rec["PostTypeId"] == '1':
                account_id = rec["OwnerUserId"]
                message.user_id = users_id[account_id]
                message.text = rec["Body"]
                message.created_date = rec["CreationDate"]
                collection.insert_one(dict(message))
        except KeyError:
            print("Key from Posts Not Found.")
