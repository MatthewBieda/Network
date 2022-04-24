from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField("self", symmetrical=False, blank=True, related_name="following")

class Post(models.Model):
    content = models.CharField(max_length=280)
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author_relation")
    likes = models.ManyToManyField(User, blank=True, related_name="likes_relation")