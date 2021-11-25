from django.db import models
from django.contrib.auth.models import User

from recipe.models import Recipe, Ingredients


class Profile(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    nick_name = models.CharField(max_length=100)

    disliked = models.ManyToManyField(Ingredients, blank=True)
    bookmark = models.ManyToManyField(Recipe, blank=True)

    def __str__(self):
        return self.nick_name
