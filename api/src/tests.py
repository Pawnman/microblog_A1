import os
import datetime
from datetime import timedelta

import random

import uuid

import requests

api_url = os.getenv('API_URL')

# def test_messages_for_day():
API_URL = "http://localhost:9200/message"

#
# def find_by_id_user():
#     return print(requests.get(f'http://localhost:9200/message/_doc').json())
#
#
# print(find_by_id_user())
user_id = '1'

print(requests.get(f'http://localhost:9200/message/filter?user_id=2').json())


#
# # def create_tweet_day(user_id=None, text=None):
# #     if user_id is None:
# #         user_id = random.randint(0, 100)
# #     if text is None:
# #         text = str(uuid.uuid4())
# #     #created_date = str(datetime.datetime.now()).split(' ')[0]
# #     created_date = f'2023-12-{random.randint(1, 31)}'
# #     response = requests.post(API_URL, json={
# #         'user_id': user_id,
# #         'text': text,
# #         'date': created_date
# #     })
# #     return response.json()
#
# api_url = "http://localhost:9200/message"
#
#
# def test_user_tweets_last_day(api_url, user_id):
#     current_date = datetime.datetime.now()
#
#     last_day_date = current_date - timedelta(days=1)
#
#     current_date_formatted = current_date.strftime('%Y-%m-%d')
#     last_day_formatted = last_day_date.strftime('%Y-%m-%d')
#
#     headers = {
#         'accept': 'application/json'
#               }
#     params = {'user_id': user_id,
#               'create_data': last_day_formatted
#               #'end_date': current_date_formatted
#              }
#     response = requests.get(api_url, headers=headers, params=params)
#     if response.status_code == 200:
#         user_tweets = response.json()
#         print(f"Твиты за последний день для пользователя с ID {user_id}:")
#         for tweet in user_tweets:
#             print(tweet)
#     else:
#         print("Ошибка при получении твитов:", response.status_code)
#         print(current_date_formatted, last_day_formatted)
#
#
# def test_user_tweets_last_hour(api_url, user_id):
#     #current_date = datetime.datetime.now()
#
#     last_day_date = current_date - timedelta(hour=1)
#
#     current_date_formatted = current_date.strftime('%Y-%m-%d %H:%M:%S')
#     last_day_formatted = last_day_date.strftime('%Y-%m-%d %H:%M:%S')
#
#     headers = {
#         'accept': 'application/json'
#               }
#     params = {'user_id': user_id,
#               'start_date': last_day_formatted,
#               'end_date': current_date_formatted
#              }
#     response = requests.get(api_url, headers=headers, params=params)
#     if response.status_code == 200:
#         user_tweets = response.json()
#         print(f"Твиты за последний час для пользователя с ID {user_id}:")
#         for tweet in user_tweets:
#             print(tweet)
#     else:
#         print("Ошибка при получении твитов:", response.status_code)
# #
# # def test_tweet_for_day_by_uid():
# #     user_id = random.randint(0, 100)
# #     text = str(uuid.uuid4())
# #     created_tweets = [create_tweet_day(user_id, text), create_tweet_day(), create_tweet_day()]

# print(test_user_tweets_last_day("http://localhost:9200/message", 1))
#
# print(requests.get("http://localhost:9200/_search?index=message").json())