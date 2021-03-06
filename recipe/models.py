from django.db import models
from django.contrib.auth.models import User
import datetime


class Ingredients(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    writer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, default=0)
    title = models.CharField(max_length=100)

    nowDate = (datetime.datetime.now()).strftime('%Y-%m-%d')
    created_date = models.CharField(max_length=100, default=nowDate)
    views = models.IntegerField(default=0)

    #thumb = models.ImageField(upload_to='thumbs', blank=True)
    thumb = models.TextField(blank=True)

    def __str__(self):
        return self.title

class Unit(models.Model):
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE,null=True, blank=True)
    ingrd_id = models.ForeignKey(Ingredients, on_delete=models.CASCADE,null=True, blank=True)
    unit = models.CharField(max_length=100)

    def __str__(self):
        return self.unit

class Steps(models.Model):
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE, blank=True)
    num = models.IntegerField(default=0)
    contents = models.CharField(max_length=1000)
    img = models.TextField(blank=True)

    def __str__(self):
        return self.contents