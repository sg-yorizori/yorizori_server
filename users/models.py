from django.db import models
from django.contrib.auth.models import User

from recipe.models import Recipe, Ingredients


class Profile(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    nick_name = models.CharField(max_length=100)
    profile_img = models.URLField(blank=True)

    disliked = models.ManyToManyField(Ingredients, blank=True)
    bookmark = models.ManyToManyField(Recipe, blank=True)
    vegan = models.IntegerField(default=0)


    def __str__(self):
        return self.nick_name
