import random

import pytest
from django.forms.models import model_to_dict

from liberty_test_task.db_services import (
    create_comments_in_db,
    create_posts_in_db,
    delete_all_posts_and_comments_in_db,
    get_all_comments_from_db,
    get_all_posts_from_db,
    get_comment_from_db,
    get_post_from_db,
)
from liberty_test_task.models import Comment, Post


@pytest.mark.django_db
def test_create_posts_in_db(posts_data):
    create_posts_in_db(posts_data)
    assert Post.objects.count() == len(posts_data)


@pytest.mark.django_db
def test_create_comments_in_db(posts_data, comments_data):
    create_posts_in_db(posts_data)
    create_comments_in_db(comments_data)
    assert Comment.objects.count() == len(comments_data)


@pytest.mark.django_db
def test_delete_all_posts_and_comments_in_db(posts_data, comments_data):
    create_posts_in_db(posts_data)
    create_comments_in_db(comments_data)
    assert Post.objects.count() == len(posts_data)
    assert Comment.objects.count() == len(comments_data)

    delete_all_posts_and_comments_in_db()
    assert Post.objects.count() == 0
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_get_post_from_db(posts_data, comments_data):
    create_posts_in_db(posts_data)
    random_post_id = random.randint(1, len(posts_data))

    expected_post_data = next(
        filter(lambda x: x["id"] == random_post_id, posts_data)
    )
    post_from_db = get_post_from_db(random_post_id)

    assert post_from_db == Post(**expected_post_data)


@pytest.mark.django_db
def test_get_all_posts_from_db(posts_data):
    create_posts_in_db(posts_data)
    all_posts_from_db = get_all_posts_from_db()
    expected_posts_data = [Post(**post_data) for post_data in posts_data]

    for post_from_db, expected_post_data in zip(
        all_posts_from_db, expected_posts_data
    ):
        assert post_from_db == expected_post_data


@pytest.mark.django_db
def test_get_comment_from_db(posts_data, comments_data):
    create_posts_in_db(posts_data)
    create_comments_in_db(comments_data)
    random_comment_id = random.randint(1, len(comments_data))

    expected_comment_data = next(
        filter(lambda x: x["id"] == random_comment_id, comments_data)
    )
    comment_from_db = get_comment_from_db(random_comment_id)

    assert comment_from_db == Comment(**expected_comment_data)


@pytest.mark.django_db
def test_get_all_comments_from_db(posts_data, comments_data):
    create_posts_in_db(posts_data)
    create_comments_in_db(comments_data)
    all_comments_from_db = get_all_comments_from_db()

    for comment_from_db in all_comments_from_db:
        expected_comment_data = next(
            filter(lambda x: x["id"] == comment_from_db.id, comments_data)
        )
        assert comment_from_db == Comment(**expected_comment_data)
