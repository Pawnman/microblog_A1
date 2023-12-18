import os
import random
import uuid
import secrets
import requests
import datetime

API_URL_POST = "http://localhost:8000/post_tweet"
API_URL_GET = "http://127.0.0.1:8000/get_tweet_by_id"
API_URL_DELETE = "http://127.0.0.1:8000/delete_tweet_by_id"

def create_tweet(user_id=None, text=None, created_date=None,created_time = None):
    if user_id is None:
        user_id = str(uuid.uuid4())
    if text is None:
        text = str(uuid.uuid4())
    if created_date is None:
        created_date = str(datetime.datetime.now()).split(' ')[0]
    if created_time is None:
        created_time = str(datetime.datetime.now()).split(' ')[1]
    params = {
        'user_id': user_id,
        'text': text,
        'created_date': created_date,
        'created_time': created_time
    }
    response = requests.post(API_URL_POST, json=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error creating student: {response.status_code}")
        return None


def test_tweet_creation_and_deletion():
    user_id = str(uuid.uuid4())
    text = str(uuid.uuid4())
    created_date = str(datetime.datetime.now()).split(' ')[0]
    created_time = str(datetime.datetime.now()).split(' ')[1]
    created_id = create_tweet(user_id, text, created_date, created_time)
    user_url = f'{API_URL_GET}/{created_id}'
    response = requests.get(user_url)
    if response.status_code == 200:
        user = response.json()
    else:
        print(f"Error: {response.status_code}")
    assert user['user_id'] == user_id
    assert user['text'] == text
    assert user['created_date'] == created_date
    assert user['created_time'] == created_time
    response = requests.delete(f"{API_URL_DELETE}/{created_id}")
    assert response.status_code == 200
    print("Success") 

if __name__ == "__main__":
    test_tweet_creation_and_deletion()
