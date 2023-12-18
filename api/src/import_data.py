import xml.etree.ElementTree as ET
import secrets
from pymongo import MongoClient
from models.message import Tweet
from models.user import User
from elasticsearch import AsyncElasticsearch
import os

CONNECTION_STRING = "mongodb://localhost:27017"
ELASTICSEARCH_URI = os.getenv('ELASTICSEARCH_URI')
USERS_PATH = r"...\...\data\xml\Users (1).xml"
TWEETS_PATH = r"...\...\data\xml\Posts.xml"
client = MongoClient(CONNECTION_STRING)
db = client["microblog"]
elasticsearch_uri = os.getenv('ELASTICSEARCH_URI')
elasticsearch_client = AsyncElasticsearch(elasticsearch_uri.split(','))

def email_generator():
    return f"{secrets.token_hex(8)}@gmail.com"

def password_generator():
    return f"{secrets.token_hex(3)}"

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
            #user_account.password = password_generator()
            user_account.created_at = rec["CreationDate"]
        except KeyError:
            print("Key from Users Not Found.")
            continue
        insert_result = collection.insert_one(dict(user_account))
        users_id[account_id] = str(insert_result.inserted_id)


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

import_user_accounts()
import_messages()
