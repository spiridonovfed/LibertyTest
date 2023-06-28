import json

import pytest


@pytest.fixture
def posts_data():
    with open("tests/posts.json") as file:
        posts_data = json.load(file)
    return posts_data


@pytest.fixture
def comments_data():
    with open("tests/comments.json") as file:
        comments_data = json.load(file)
    return comments_data
