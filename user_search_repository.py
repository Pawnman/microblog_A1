from elasticsearch import AsyncElasticsearch
from fastapi import Depends
class UserSearchRepository:
    _elasticsearch_client: AsyncElasticsearch
    _elasticsearch_index: str

    def __init__(self,
                 elasticsearch_index: str,
                 elasticsearch_client: AsyncElasticsearch):
        self._elasticsearch_index = elasticsearch_index
        self._elasticsearch_client = elasticsearch_client

    async def get_by_name(self, name: str) -> list[User]:
        query = {}
        # query дополняется ровно тем шаблоном, который отправляется в качестве карточки
        response = await self._elasticsearch_client.search(index=self._elasticsearch_index, query=query, filter_path=)
        # filter_path ограничивет количество полей, которые будут выводится в результате поиска
    @staticmethod
    def get_instance(elasticsearch_client: AsyncElasticsearch = Depends(get_elasticsearch_client)):
        elasticsearch_index = os.getenv('ELASTICSEARCH_INDEX')
        return UserSearchRepository(elasticsearch_index, elasticsearch_client)