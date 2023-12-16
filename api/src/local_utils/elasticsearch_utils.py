import os
from elasticsearch import AsyncElasticsearch

elasticsearch_client: AsyncElasticsearch = None


def get_elasticsearch_client() -> AsyncElasticsearch:
    return elasticsearch_client


# Запуск ElasticSearch и подключение к порту с проверкой успешности подключения
async def connect_and_init_elasticsearch():
    global elasticsearch_client
    elasticsearch_uri = os.getenv('ELASTICSEARCH_URI')
    try:
        elasticsearch_client = AsyncElasticsearch(elasticsearch_uri.split(','))
        await elasticsearch_client.info()
        print(f'Connected to elasticsearch with uri: {elasticsearch_uri}', flush=True)

    except Exception as ex:
        print(f'Cant connect to elasticsearch: {ex}', flush=True)


# Закрытие ElasticSearch
async def close_connection_elasticsearch():
    global elasticsearch_client
    if elasticsearch_client is None:
        return
    await elasticsearch_client.close()
