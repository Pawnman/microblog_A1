import os
from datetime import datetime, timedelta

from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from .elasticsearch_utils import elasticsearch_client, get_elasticsearch_client
from models.user import User, UserUpdate
from models.message import Tweet, TweetUpdate


class UserSearchRepository: # delete
    _elasticsearch_client: AsyncElasticsearch
    _elasticsearch_users_index: str
    _elasticsearch_messages_index: str

class MessageSearchRepository(): #rename SearchRepository
    _elasticsearch_client: AsyncElasticsearch
    _elasticsearch_users_index: str
    _elasticsearch_messages_index: str

    def __init__(self, index_users: str, index_messages: str, client: AsyncElasticsearch):
        self._elasticsearch_client = client
        self._elasticsearch_users_index = index_users
        self._elasticsearch_messages_index = index_messages

    async def get_by_name(self, name: str) -> list[User]:
        index_exist = await self._elasticsearch_client.indices.exists(index=self._elasticsearch_users_index)
        if not index_exist:
            return []

        query = { "match": {
                    "name": {"query": name}}
                }
        response = await self._elasticsearch_client.search(index=self._elasticsearch_users_index,
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

    # у пользователя всегда уникальный email, иначе не получится создать аккаунт. НПроследить за точностью
    async def get_by_email(self, email: str) -> list[User]: #testing
        index_exist = await self._elasticsearch_client.indices.exists(index=self._elasticsearch_users_index)
        if not index_exist:
            return []
            
        query = { "match": {
                    "email": {"query": email}}
                }
        response = await self._elasticsearch_client.search(index=self._elasticsearch_users_index,
                                                            query=query,
                                                            filter_path=['hits.hits._id', 'hits.hits._source'])
        if 'hits' not in response.body:
            return []

        result = response.body['hits']['hits']
        user = list(map(lambda user: User(id=user['_id'],
                                           name=user['_source']['name'],
                                           age=user['_source']['age'],
                                           email=user['_source']['email'],
                                           creaated_at=user['_source']['created_at'],
                                           ), result))
        
        return user

    async def find_tweet(self, user_id: str, pattern: str) -> list[Tweet]: #testing
        index_exist = await self._elasticsearch_client.indices.exists(
                                                        index=self._elasticsearch_messages_index)
        if not index_exist:
            return []
        query = {'bool': {'must': [
                        {'bool': {'should': [
                                {'bool': {'must': [
                                    {"match": {"user_id": {"query": user_id}}},
                                    {"match": {"text": {"query": pattern,
                                                        "fuzziness": 2,
                                                        "prefix_length": 1}}}
                ]}}]}}]}}
        response = await self._elasticsearch_client.search(index=self._elasticsearch_messages_index,
                                                    query=query,
                                                    filter_path=['hits.hits._id', 'hits.hits._source'])
        if 'hits' not in response.body:
            return []
        result = response.body['hits']['hits']
        tweets = list(map(lambda tweet: Tweet(id=tweet['_id'],
                                            user_id=tweet['_source']['user_id'],
                                            text=tweet['_source']['text'],
                                            created_date=tweet['_source']['created_date'],
                                            created_time=tweet['_source']['created_time']
                                            ), result))
        return tweets

    async def search_tweet_last_day(self, user_id: str) -> list[Tweet]:
        delta_date = str(datetime.now() - timedelta(days=1)).split(' ')[0]
        print(delta_date)

        query = {'bool': {'must': [
                        {'match': {"user_id": {"query": user_id}}}],
                        'filter': [
                                  {"range": {"created_date": {"gte": delta_date}}}]
                }}
        response = await self._elasticsearch_client.search(index=self._elasticsearch_messages_index,
                                                     query=query,
                                                     filter_path=['hits.hits._id', 'hits.hits._source'])

        if 'hits' not in response.body:
            return []
        result = response.body['hits']['hits']
        tweets = list(map(lambda tweet: Tweet(id=tweet['_id'],
                                            user_id=tweet['_source']['user_id'],
                                            text=tweet['_source']['text'],
                                            created_time=tweet['_source']['created_time'],
                                            created_date=tweet['_source']['created_date']
                                            ), result))
        return tweets

    async def search_tweet_last_hour(self, user_id: str) -> list[Tweet]:
        delta_date = str(datetime.now() - timedelta(days=1)).split(' ')[0]
        delta_time = str(datetime.now() - timedelta(hours=1)).split(' ')[1]
        print(delta_time)

        query = {'bool': {'must': [
                            {'match': {"user_id": {"query": user_id}}}],
                            'filter': [
                                    {"range": { "created_date": { "gte": delta_date}}},
                                    {"range": { "created_time": { "gte": delta_time}}}]
                }}
        response = await self._elasticsearch_client.search(index=self._elasticsearch_messages_index,
                                                     query=query,
                                                     filter_path=['hits.hits._id', 'hits.hits._source'])

        if 'hits' not in response.body:
            return []
        result = response.body['hits']['hits']
        tweets = list(map(lambda tweet: Tweet(id=tweet['_id'],
                                            user_id=tweet['_source']['user_id'],
                                            text=tweet['_source']['text'],
                                            created_time=tweet['_source']['created_time'],
                                            created_date=tweet['_source']['created_date']
                                            ), result))
        return tweets

    async def create_user(self, user_id: str, user: User):
        await self._elasticsearch_client.create(index=self._elasticsearch_users_index,
                                                                    id=user_id, document=dict(user))

    async def update_user(self, user_id: str, user: User):
        await self._elasticsearch_client.update(index=self._elasticsearch_users_index,
                                                                    id=user_id, doc=dict(user)) #testing
        print(f"updated to elastic")

    async def delete_user(self, user_id: str):
        await self._elasticsearch_client.delete(index=self._elasticsearch_users_index, id=user_id)  #testing

    async def create_message(self, tweet_id: str, message: Tweet):
        await self._elasticsearch_client.create(index=self._elasticsearch_messages_index, id=tweet_id,
                                          document=dict(message))
    async def delete_message(self, tweet_id: str):
        await self._elasticsearch_client.delete(index=self._elasticsearch_messages_index, id=tweet_id)  #testing
        

    async def update_message(self, tweet_id: str, message: Tweet):
        print(f" begin updating to elastic")
        await self._elasticsearch_client.update(index=self._elasticsearch_messages_index,
                                                                    id=tweet_id, doc=dict(message)) #testing
        print(f"updated to elastic")


    @staticmethod
    def get_instance(client: AsyncElasticsearch = Depends(get_elasticsearch_client)):
        elasticsearch_user_index = os.getenv('ELASTICSEARCH_USER_INDEX')
        elasticsearch_messages_index = os.getenv('ELASTICSEARCH_MESSAGE_INDEX')
        return MessageSearchRepository(elasticsearch_user_index, elasticsearch_messages_index, client)