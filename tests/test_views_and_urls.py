import random

import pytest
import responses
from django.core.cache import cache

from liberty_test_task.db_services import (
    create_comments_in_db,
    create_posts_in_db,
)
from liberty_test_task.models import Comment, Post
from liberty_test_task.settings import GET_COMMENTS_URL, GET_POSTS_URL


@responses.activate
@pytest.mark.django_db
def test_refetch_posts_and_comments_positive(
    client, posts_data, comments_data
):
    responses.add(responses.GET, GET_POSTS_URL, status=200, json=posts_data)
    responses.add(
        responses.GET, GET_COMMENTS_URL, status=200, json=comments_data
    )

    url = "http://localhost/refetch_posts_and_comments"
    response = client.get(url)
    assert response.status_code == 200
    assert Post.objects.count() == len(posts_data)
    assert Comment.objects.count() == len(comments_data)


@responses.activate
@pytest.mark.django_db
def test_refetch_posts_and_comments_no_connection(client):
    url = "http://localhost/refetch_posts_and_comments"
    response = client.get(url)
    assert response.status_code == 404


@pytest.mark.django_db
def tests_get_posts(client, posts_data, comments_data):
    create_posts_in_db(posts_data)
    create_comments_in_db(comments_data)

    url = "http://localhost/posts"
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.json()) == len(posts_data)

    expected_comments_data = comments_data.copy()
    for comment in expected_comments_data:
        comment_obj = comment["postId"]
        comment["postId"] = comment_obj.id

    for post_from_response in response.json():
        expected_post_data = [
            post_data
            for post_data in posts_data
            if post_data["id"] == post_from_response["id"]
        ][0]
        expected_relevant_comments = [
            comment_data
            for comment_data in expected_comments_data
            if comment_data["postId"] == expected_post_data["id"]
        ]
        assert post_from_response["comments"] is not None
        assert len(post_from_response["comments"]) == len(
            expected_relevant_comments
        )


@pytest.mark.django_db
def test_get_post_positive(client, posts_data, comments_data):
    create_posts_in_db(posts_data)
    create_comments_in_db(comments_data)
    random_post_id = random.randint(1, len(posts_data))
    url = f"http://localhost/posts/{random_post_id}"
    response = client.get(url)
    response_content = response.json()
    assert response.status_code == 200
    assert response_content["comments"] is not None

    expected_comments_data = comments_data.copy()
    for comment in expected_comments_data:
        comment_obj = comment["postId"]
        comment["postId"] = comment_obj.id
    expected_relevant_comments = [
        comment_data
        for comment_data in expected_comments_data
        if comment_data["postId"] == response_content["id"]
    ]

    assert len(response_content["comments"]) == len(expected_relevant_comments)


@pytest.mark.django_db
def test_get_post_no_such_post(client, posts_data, comments_data):
    create_posts_in_db(posts_data)
    create_comments_in_db(comments_data)
    non_existing_post_id = len(posts_data) + 1
    url = f"http://localhost/posts/{non_existing_post_id}"
    response = client.get(url)
    assert response.status_code == 404
    assert (
        response.json()
        == f"Post with id {non_existing_post_id} does not exist"
    )


@pytest.mark.django_db
def test_get_comments(client, posts_data, comments_data):
    create_posts_in_db(posts_data)
    create_comments_in_db(comments_data)

    url = "http://localhost/comments"
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.json()) == len(comments_data)


@pytest.mark.django_db
def test_get_comment_positive(client, posts_data, comments_data):
    create_posts_in_db(posts_data)
    create_comments_in_db(comments_data)
    random_comment_id = random.randint(1, len(comments_data))

    url = f"http://localhost/comments/{random_comment_id}"
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_comment_no_such_comment(client, posts_data, comments_data):
    create_posts_in_db(posts_data)
    create_comments_in_db(comments_data)
    non_existing_comment_id = len(comments_data) + 1

    url = f"http://localhost/comments/{non_existing_comment_id}"
    response = client.get(url)
    assert response.status_code == 404
    assert (
        response.json()
        == f"Comment with id {non_existing_comment_id} does not exist"
    )
