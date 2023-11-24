"""
Before running this script, Django server must be running.
Command:  python manage.py runserver
"""

import os
import random
import csv
from uuid import uuid4

from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_network.settings')
import django
django.setup()
import requests
from django.db.models import Subquery
from apps.post.models import PostLike, Post
from apps.authentication.models import RegistrationOTC
User = get_user_model()


def main():
    data_dict = {}
    with open("config.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            key = row[0].strip()
            value = int(row[1].strip())
            data_dict[key] = value

    for user in range(data_dict["number_of_users"]):
        user = create_user()
        if user:
            amount_posts = random.randint(0, data_dict["max_posts_per_user"])
            amount_likes = random.randint(0, data_dict["max_likes_per_user"])
            for post in range(amount_posts):
                create_post(user)
            for like in range(amount_likes):
                create_like(user)


def create_user():
    url_send_registration_code = "http://127.0.0.1:8000/api/auth/registration-send-code/"
    url_confirm_registration_code = "http://127.0.0.1:8000/api/auth/registration-validate-code/"
    url_create_user = "http://127.0.0.1:8000/api/auth/registration-create-user/"
    email = f"user{uuid4()}@example.com"
    password = str(uuid4())
    response_send_registration_code = requests.post(url=url_send_registration_code, data={"email": email})
    if response_send_registration_code.status_code != 201:
        print(f"response_send_registration_code {response_send_registration_code.status_code}")
        return None
    otc_code = RegistrationOTC.objects.get(email=response_send_registration_code.json()["email"]).code
    response_confirm_registration_code = requests.post(
        url=url_confirm_registration_code,
        data={"email": email, "code": otc_code}
    )
    if response_confirm_registration_code.status_code != 201:
        print(f"response_confirm_registration_code {response_confirm_registration_code.status_code}")
        return None
    response_create_user = requests.post(
        url=url_create_user,
        data={"email": email, "password": password, "password_confirmation": password}
    )
    if response_create_user.status_code != 201:
        print(f"response_create_user {response_create_user.status_code}")
        return None
    response_with_mail = response_create_user.json()
    response_with_mail["email"] = email
    return response_with_mail


def create_post(tokens: dict = None):
    if tokens is None:
        return None
    url_create_post = "http://127.0.0.1:8000/api/post/"
    text = str(uuid4())
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    response_create_post = requests.post(
        url=url_create_post,
        data={"text": text},
        headers=headers,
    )
    return response_create_post.status_code


def create_like(tokens: dict = None):
    if tokens is None:
        return None
    url_create_like = "http://127.0.0.1:8000/api/post/like/"
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    user = User.objects.get(email=tokens["email"])
    liked_posts_subquery = PostLike.objects.filter(user=user).values('post__id')
    posts_not_liked = Post.objects.exclude(id__in=Subquery(liked_posts_subquery))
    if posts_not_liked.exists():
        random_post = random.choice(posts_not_liked)
        post_id = random_post.id
        response_create_like = requests.post(
            url=url_create_like,
            data={"post_id": post_id},
            headers=headers,
        )
        return response_create_like.status_code
    return None


if __name__ == '__main__':
    main()

