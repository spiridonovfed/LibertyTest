import pytest
import responses
from requests.exceptions import RequestException

from liberty_test_task.requests_services import (
    fetch_comments,
    fetch_data,
    fetch_posts,
)
from liberty_test_task.settings import GET_COMMENTS_URL, GET_POSTS_URL


@responses.activate
def test_fetch_data_positive(posts_data):
    responses.add(responses.GET, GET_POSTS_URL, status=200, json=posts_data)
    response = fetch_data(GET_POSTS_URL)
    assert response == posts_data


@responses.activate
def test_fetch_data_no_connection():
    with pytest.raises(RequestException):
        fetch_data(GET_POSTS_URL)


@responses.activate
def test_fetch_posts_positive(posts_data):
    responses.add(responses.GET, GET_POSTS_URL, status=200, json=posts_data)
    fetched_posts = fetch_posts()
    assert fetched_posts == posts_data


@responses.activate
def test_fetch_comments_positive(comments_data):
    responses.add(
        responses.GET, GET_COMMENTS_URL, status=200, json=comments_data
    )
    fetched_comments = fetch_comments()
    assert fetched_comments == comments_data
