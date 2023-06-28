from liberty_test_task.logger import Logger

from .models import Comment, Post


def create_posts_in_db(fetched_posts):
    Logger.info("Creating %s posts in db", len(fetched_posts))
    post_objects = [Post(**fetched_post) for fetched_post in fetched_posts]

    Post.objects.bulk_create(post_objects)
    Logger.info("%s posts are created in db", len(fetched_posts))


def create_comments_in_db(fetched_comments):
    Logger.info("Creating %s comments in db", len(fetched_comments))
    comment_objects = []

    for fetched_comment in fetched_comments:
        relevant_post_id = fetched_comment["postId"]
        fetched_comment["postId"] = Post.objects.get(pk=relevant_post_id)
        comment_obj = Comment(**fetched_comment)
        comment_objects.append(comment_obj)

    Comment.objects.bulk_create(comment_objects)
    Logger.info("%s comments are created in db", len(fetched_comments))


def delete_all_posts_and_comments_in_db():
    Comment.objects.all().delete()
    Logger.info("All comments in db are deleted")
    Post.objects.all().delete()
    Logger.info("All posts in db are deleted")


def get_post_from_db(id):
    return Post.objects.get(pk=id)


def get_all_posts_from_db():
    return Post.objects.all()


def get_comment_from_db(id):
    return Comment.objects.get(pk=id)


def get_all_comments_from_db():
    return Comment.objects.all()
