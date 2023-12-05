import os
from datetime import datetime, timedelta

from elasticsearch import AsyncElasticsearch
#from fastapi import Depends

from elasticsearch_utils import elasticsearch_client
from models.user import User, UserUpdate
from models.message import Tweet


class UserSearchRepository:
    _elasticsearch_client: AsyncElasticsearch
    _elasticsearch_users_index: str
    _elasticsearch_messages_index: str


class MessageSearchRepository():
    def __init__(self):
        self._elasticsearch_users_index = os.getenv('ELASTICSEARCH_USER_INDEX')
        self._elasticsearch_messages_index = os.getenv('ELASTICSEARCH_MESSAGE_INDEX')

    # def __init__(self,
    #              elasticsearch_index: str,
    #              elasticsearch_client: AsyncElasticsearch):
    #     self._elasticsearch_index = elasticsearch_index
    #     self._elasticsearch_client = elasticsearch_client

    async def get_by_name(self, name: str) -> list[User]:
        query = {
            "match":
                {
                    "name":
                        {
                            "query": name
                        }
                }
        }
        response = await elasticsearch_client.search(index=self._elasticsearch_users_index,
                                                     query=query,
                                                     filter_path=['hits.hits._id', 'hits.hits._source'])
        if 'hits' not in response.body:
            return []
        result = response.body['hits']['hits']
        users = list(map(lambda user: User(id=user['_id'],
                                           name=user['_source']['name'],
                                           age=user['_source']['age'],
                                           email=user['_source']['email'],
                                           creaated_at=user['_source']['created_at'],
                                           ), result))
        return users

    async def get_by_email(self, email: str) -> list[User]:
        query = {
            "match":
                {
                    "username":
                     {
                         "query": email
                     }
                }
        }
        response = await elasticsearch_client.search(index=self._elasticsearch_users_index,
                                                     query=query,
                                                     filter_path=['hits.hits._id', 'hits.hits._source'])
        if 'hits' not in response.body:
            return []
        result = response.body['hits']['hits']

        users = list(map(lambda user: User(id=user['_id'],
                                           name=user['_source']['name'],
                                           age=user['_source']['age'],
                                           email=user['_source']['email'],
                                           creaated_at=user['_source']['created_at'],
                                           ), result))
        return users

    async def find_tweet(self, user_id: str, pattern: str) -> list[Tweet]:
        query = {'bool': {'must': [
            {'bool': {'should': [
                {'bool':
                     {'must': [{"match": {"user_id": {"query": user_id}}},
                     {"match": {"content.text_content": {"query": pattern}}}]}
                }]}}]}}

        response = await elasticsearch_client.search(index=self._elasticsearch_messages_index,
                                                     query=query,
                                                     filter_path=['hits.hits._id', 'hits.hits._source'])
        if 'hits' not in response.body:
            return []
        result = response.body['hits']['hits']
        tweets = list(map(lambda tweet: Tweet(id=tweet['_id'],
                                              user_id=tweet['_source']['user_id'],
                                              text=tweet['_source']['text'],
                                              post_date=tweet['_source']['post_date']), result))
        return tweets

    async def search_last_day(self, user_id: str) -> list[Tweet]:
        time_before = datetime.now() - timedelta(hours=1)
        time_before = str(time_before)

        query = {'bool': {'must': [{'match': {"user_id": {"query": user_id}}}],
                          'filter': [
                                  {"range": {
                                      "created_time": {
                                          "gte": {time_before}}}}]
                              }
                     }
        response = await elasticsearch_client.search(index=self._elasticsearch_messages_index,
                                                     query=query,
                                                     filter_path=['hits.hits._id', 'hits.hits._source'])

        if 'hits' not in response.body:
            return []
        result = response.body['hits']['hits']
        tweets = list(map(lambda tweet: Tweet(id=tweet['_id'],
                                              user_id=tweet['_source']['user_id'],
                                              text=tweet['_source']['text'],
                                              created_time=tweet['_source']['created_time'],
                                              created_date=tweet['_source']['created_date']), result))
        return tweets

    async def search_last_hour(self, user_id: str) -> list[Tweet]:
        time_before = datetime.now() - timedelta(hours=1)
        time_before = str(time_before)

        query = {'bool': {'must': [{'match': {"user_id": {"query": user_id}}}],
                          'filter': [
                              {"range": {
                                  "created_time": {
                                      "gte": {time_before}}}}]
                          }
                 }
        response = await elasticsearch_client.search(index=self._elasticsearch_messages_index,
                                                     query=query,
                                                     filter_path=['hits.hits._id', 'hits.hits._source'])

        if 'hits' not in response.body:
            return []
        result = response.body['hits']['hits']
        tweets = list(map(lambda tweet: Tweet(id=tweet['_id'],
                                              user_id=tweet['_source']['user_id'],
                                              text=tweet['_source']['text'],
                                              created_time=tweet['_source']['created_time'],
                                              created_date=tweet['_source']['created_date']), result))
        return tweets

    # Есть сомнения в типе данных doc(user)
    async def create_user(self, user_id: str, user: UserUpdate):
        await elasticsearch_client.create(index=self._elasticsearch_users_index, id=user_id, doc=user)

    async def update_user(self, user_id: str, user: UserUpdate):
        await elasticsearch_client.update(index=self._elasticsearch_users_index, id=user_id, doc=user)

    async def delete_user(self, user_id: str):
        await elasticsearch_client.delete(index=self._elasticsearch_users_index, id=user_id)

    async def create_message(self, tweet_id: str, message: Tweet):
        await elasticsearch_client.create(index=self._elasticsearch_messages_index, id=tweet_id,
                                          doc=message)
    @staticmethod
    def get_instance():
        # elasticsearch_user_index = os.getenv('ELASTICSEARCH_USER_INDEX')
        # elasticsearch_messages_index = os.getenv('ELASTICSEARCH_MESSAGE_INDEX')
        return MessageSearchRepository()