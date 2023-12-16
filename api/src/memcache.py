from pymemcache import HashClient
from pymemcache.client.base import Client

import os

from json_serializer import JsonSerializer

memcached_client: Client = None


memcached_user_client: HashClient = None
memcached_message_client: HashClient = None


def connection_and_init_memcached():
    global memcached_user_client
    global memcached_message_client
    
    memcached_user_uri = os.getenv('MEMCACHED_USER_URI')
    memcached_message_uri = os.getenv('MEMCACHED_MESSAGE_URI')
    
    memcached_uris = [memcached_user_uri, memcached_message_uri]
    
    memcached_clients = [None for _ in range(2)]
    
    for i, (memcached_client, memcached_uri) in enumerate(zip(memcached_clients, memcached_uris)):
        print(f'step {i}; clients = {memcached_client}; uris = {memcached_uri}', flush=True)
        
        try:
            memcached_clients[i] = HashClient(memcached_uri.split(','), serde=JsonSerializer())
            print(f'Connected to memcached with uri {memcached_uri}', flush=True)
        except Exception as ex:
            print(f'Cant connect to memcached: {ex}')


def close_memcached_connection():
    global memcached_user_client
    global memcached_message_client
    
    memcached_clients = [memcached_client, memcached_message_client]
    
    for memcahced_client in memcached_clients:
        if memcahced_client is not None:
            memcached_client.close()
    
    
def get_memcached_user_client():
    return memcached_user_client


def get_memcached_message_client():
    return memcached_message_client
