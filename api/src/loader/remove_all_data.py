from pymongo import MongoClient
from pydantic import BaseModel
from elasticsearch import Elasticsearch

CONNECTION_STRING = "mongodb://localhost:27017"
client = MongoClient(CONNECTION_STRING)
db = client["microblog"]

elasticsearch_uri = "http://localhost:9200"
elasticsearch_client = Elasticsearch(elasticsearch_uri)
elasticsearch_users_index = "useraccount"
elasticsearch_messages_index = "message"



def delete_messages():
    collection = db["Message"]
    collection.drop()
    elasticsearch_client.delete_by_query(index=elasticsearch_messages_index, body={"query": {"match_all": {}}})
    

def delete_users():
    collection = db["UserAccount"]
    collection.drop()
    elasticsearch_client.delete_by_query(index=elasticsearch_users_index, body={"query": {"match_all": {}}})

delete_users()
delete_messages()