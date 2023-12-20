import os
import datetime
from datetime import timedelta

import random
import uuid
import requests

api_url = 'http://localhost:9200' + '/message'


def create_tweet(user_id=None, text=None):
    if user_id is None:
        user_id = str(random.randint(1, 100))
    if text is None:
        text = str(uuid.uuid4())
    created_date = str(datetime.datetime.now()).split(' ')[0]
    created_time = str(datetime.datetime.now())
    response = requests.post(api_url, json={
        'user_id': user_id,
        'text': text,
        "created_date": created_date,
        "created_time": created_time
    })
    return response.json()


# Тест на поиск всех твитов по id пользователя
def test_search_tweets_by_user_id():
    user_id = str(random.randint(17, 25))
    #text = 'Тестовый текст'
    #created_ids = [create_tweet(user_id, text), create_tweet(), create_tweet()]
    response = requests.get(f'{api_url}/_search?q=user_id:{user_id}')
    if response.status_code == 200 or response.status_code == 201:
        print(f"Твиты пользователя с ID {user_id}:")
        print(response.json())
    else:
        print("Ошибка при получении твитов:", response.status_code)


# Тест на поиск твитов по паттерну
def test_get_tweets_by_pattern():
    #user_id = str(random.randint(1, 100))
    pattern = "тестовый текст"
    #created_ids = [create_tweet(user_id, pattern), create_tweet(), create_tweet()]
    response = requests.get(f'{api_url}/_search?q=text:{pattern}')
    if response.status_code == 200 or response.status_code == 201:
        print(f"Твиты за с паттерном {pattern}:")
        print(response.json())
    else:
        print("Ошибка при получении твитов:", response.status_code)


# Тест на поиск твитов за последний(предыдущий день)
def test_get_tweets_for_day():
    #user_id = str(random.randint(1, 100))
    #pattern = "тестовый текст"
    tweets_for_day = str(datetime.datetime.now() - timedelta(days=1)).split(' ')[0]
    #created_ids = [create_tweet(user_id, pattern), create_tweet(), create_tweet()]
    response = requests.get(f'{api_url}/_search?q=created_date:{tweets_for_day}')
    if response.status_code == 200 or response.status_code == 201:
        print(f"Твиты за предыдущий день {tweets_for_day}:")
        print(response.json())
    else:
        print("Ошибка при получении твитов:", response.status_code)


print(test_get_tweets_by_pattern())

