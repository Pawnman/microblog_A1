import os
from elasticsearch import AsyncElasticsearch

elasticsearch_client: AsyncElasticsearch = None

def get_elasticsearch_client():
    return elasticsearch_client

async def connect_elasticsearch_and_init():
    global elasticsearch_client
    elasticsearch_uri = os.getenv('ELASTICSEARCH_URI')

    try:
        elasticsearch_client = AsyncElasticsearch(elasticsearch_uri.split(','))
        await elasticsearch_client.info()
        print(f'Connected to elasticsearch with uri: {elasticsearch_uri}')
    except Exception as ex:
        print((f'Cant connect to elasticsearch: {ex}'))

async def close_elasticsearch_connect():
    global elasticsearch_client
    if elasticsearch_client is None:
        return
    await elasticsearch_client.close()
    #pass