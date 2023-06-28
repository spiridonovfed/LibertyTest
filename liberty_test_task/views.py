import requests
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from liberty_test_task import db_services, requests_services

from .models import Comment, Post
from .serializer import CommentSerializer, PostSerializer


@api_view(["GET"])
def refetch_posts_and_comments(request):
    try:
        fetched_posts = requests_services.fetch_posts()
        fetched_comments = requests_services.fetch_comments()
    except requests.RequestException as e:
        return Response(
            data=f"Error occurred during fetching posts and comments - {e}",
            status=status.HTTP_404_NOT_FOUND,
        )

    db_services.delete_all_posts_and_comments_in_db()
    db_services.create_posts_in_db(fetched_posts)
    db_services.create_comments_in_db(fetched_comments)
    cache.clear()

    return Response(status=status.HTTP_200_OK)


@cache_page(timeout=None)
@api_view(["GET"])
def get_posts(request):
    posts = db_services.get_all_posts_from_db()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@cache_page(timeout=None)
@api_view(["GET"])
def get_post(request, id):
    try:
        post = db_services.get_post_from_db(id=id)
    except Post.DoesNotExist:
        return Response(
            data=f"Post with id {id} does not exist",
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = PostSerializer(post)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_comments(request):
    posts = db_services.get_all_comments_from_db()
    serializer = CommentSerializer(posts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_comment(request, id):
    try:
        post = db_services.get_comment_from_db(id=id)
    except Comment.DoesNotExist:
        return Response(
            data=f"Comment with id {id} does not exist",
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = CommentSerializer(post)
    return Response(serializer.data, status=status.HTTP_200_OK)
