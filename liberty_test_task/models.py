from django.db import models


class Post(models.Model):
    id = models.IntegerField(primary_key=True)
    userId = models.IntegerField()
    title = models.CharField()
    body = models.TextField()


class Comment(models.Model):
    postId = models.ForeignKey(
        to=Post, on_delete=models.CASCADE, related_name="comments"
    )
    id = models.IntegerField(primary_key=True)
    name = models.CharField()
    email = models.EmailField()
    body = models.TextField()
