import os

from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from utils.elasticsearch_utils import elasticsearch_client
from models.user import User, UserUpdate  
from models.message import Message
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
    # async def find_message(self, user_id: str, companion_id: str, pattern: str) -> list[Message]:
    #     query = {'bool': {'must': [
    #         {'bool': {'should': [
    #             {'bool': {'must': [{"match": {"sender_id": {"query": user_id}}},
    #                                {"match": {"receiver_id": {"query": companion_id}}}]}},
    #             # либо user_id - отправитель, а companion_id - получатель
    #             {'bool': {'must': [{"match": {"sender_id": {"query": companion_id}}},
    #                                {"match": {"receiver_id": {"query": user_id}}}]}}  # либо наоборот
    #         ]}},
    #         {"match": {"content.text_content": {"query": pattern}}}  # найти слова в сообщении
    #     ]}}
    #     response = await elasticsearch_client.search(index=self._elasticsearch_messages_index,
    #                                                  query=query,
    #                                                  filter_path=['hits.hits._id', 'hits.hits._source'])
    #     if 'hits' not in response.body:
    #         return []
    #     response_messages = response.body['hits']['hits']
    #     messages = list(map(lambda message: Message(id=message['_id'],
    #                                                 sender_id=message['_source']['sender_id'],
    #                                                 receiver_id=message['_source']['receiver_id'],
    #                                                 content=MessageContent(
    #                                                     text_content=message['_source']['content']['text_content']),
    #                                                 post_date=message['_source']['post_date']), response_messages))
    #     return messages
    # async def get_by_name(self, name: str) -> list[User]:
    #     query = {}
    #     # query дополняется ровно тем шаблоном, который отправляется в качестве карточки
    #     response = await self._elasticsearch_client.search(index=self._elasticsearch_index, query=query, filter_path=)
    #     # filter_path ограничивет количество полей, которые будут выводится в результате поиска
    @staticmethod
    # def get_instance(elasticsearch_client: AsyncElasticsearch = Depends(get_elasticsearch_client)):
    #     elasticsearch_index = os.getenv('ELASTICSEARCH_INDEX')
    #     return UserSearchRepository(elasticsearch_index, elasticsearch_client)