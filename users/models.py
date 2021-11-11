from django.db import models
from django.contrib.auth.models import User

from recipe.models import Recipe


class Profile(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    nick_name = models.CharField(max_length=100)
    disliked = models.CharField(max_length=200)
    #bookmark = models.ManyToManyField(Recipe, related_name="marked")

    def __str__(self):
        return self.nick_name
