import os
import random
import uuid
import secrets
import requests
import datetime


API_URL_POST = "http://localhost:8000/post_user_account"
API_URL_GET = "http://localhost:8000/get_user_account_by_id"
API_URL_DELETE = "http://localhost:8000/delete_user_by_id"
API_URL_FOLLOW = "http://127.0.0.1:8000/follow"
API_URL_UNFOLLOW = "http://127.0.0.1:8000/unfollow"
API_URL_BAN = "http://127.0.0.1:8000/ban"

def create_user(name=None, age=None, email=None,created_at = None, active = True):
    if name is None:
        name = str(uuid.uuid4())
    if age is None:
        age = random.randint(17, 25)
    if email is None:
        email = str(secrets.token_hex(2))+"@gmail.com"
    if created_at is None:
        created_at = str(datetime.datetime.now()).split(' ')[0]
    params = {
        'name': name,
        'age': age,
        'email': email,
        'created_at': created_at,
        'followers' : [],
        'following'  : [],
        'active' : active,
    }
    response = requests.post(API_URL_POST, json=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error creating student: {response.status_code}")
        return None


def test_user_creation_and_deletion():
    name = str(uuid.uuid4())
    age = random.randint(17, 25)
    email = str(secrets.token_hex(6))+"@gmail.com"
    created_at = str(datetime.datetime.now()).split(' ')[0]
    user_id = create_user(name, age, email, created_at)
    user_url = f'{API_URL_GET}/{user_id}'
    response = requests.get(user_url)
    if response.status_code == 200:
        user = response.json()
    else:
        print(f"Error: {response.status_code}")
    assert user['name'] == name
    assert user['age'] == age
    assert user['email'] == email
    assert user['created_at'] == created_at
    response = requests.delete(f"{API_URL_DELETE}/{user_id}")
    assert response.status_code == 200
    print("Success") 

'''
def test_search_users_by_email():
    name = str(uuid.uuid4())
    age = random.randint(17, 25)
    email = str(secrets.token_hex(6))+"@gmail.com"
    created_at = str(datetime.datetime.now()).split(' ')[0]
    user_id = create_user(name, age, email, created_at)
    response = requests.get(f"http://localhost:8000/filter?email={email}")
    print(response.text)
    
    assert response.status_code == 200
    data = response.json()
    user = []
    print(email)
    for doc in data:
        print(doc)
        if doc["email"] == email:
            user = doc
    
    assert user['name'] == name
    assert user['age'] == age
    assert user['email'] == email
    assert user['created_at'] == created_at
    requests.delete(f'{API_URL_DELETE}/{user_id}')
    print("Success")
'''
def test_follow_unfollow():
    name = str(uuid.uuid4())
    age = random.randint(17, 25)
    email = str(secrets.token_hex(6))+"@gmail.com"
    created_at = str(datetime.datetime.now()).split(' ')[0]
    user_id1 = create_user(name, age, email, created_at)
    name = str(uuid.uuid4())
    age = random.randint(17, 25)
    email = str(secrets.token_hex(6))+"@gmail.com"
    created_at = str(datetime.datetime.now()).split(' ')[0]
    user_id2 = create_user(name, age, email, created_at)
    url = f"{API_URL_FOLLOW}/{user_id1}/to/{user_id2}"
    response = requests.put(url)
    assert response.status_code == 200
    url = url = f"{API_URL_UNFOLLOW}/{user_id1}/from/{user_id2}"
    response = requests.put(url)
    assert response.status_code == 200
    requests.delete(f"{API_URL_DELETE}/{user_id1}")
    requests.delete(f"{API_URL_DELETE}/{user_id2}")
    print("Success")

def test_ban_unban():
    name = str(uuid.uuid4())
    age = random.randint(17, 25)
    email = str(secrets.token_hex(6))+"@gmail.com"
    created_at = str(datetime.datetime.now()).split(' ')[0]
    user_id = create_user(name, age, email, created_at)
    url = f"{API_URL_BAN}/{user_id}?state=false"
    response = requests.put(url)
    assert response.status_code == 200
    url = f"{API_URL_BAN}/{user_id}?state=true"
    response = requests.put(url)
    assert response.status_code == 200
    requests.delete(f"{API_URL_DELETE}/{user_id}")
    print("Success")

if __name__ == "__main__":
    test_user_creation_and_deletion()
    test_follow_unfollow()
    test_ban_unban()
    #test_search_users_by_email()