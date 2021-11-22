from django.db import models
from django.contrib.auth.models import User

class Ingred(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    writer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    title = models.CharField(max_length=100)

    #views는 일단 나중에 할까용
    #ingredients = models.CharField(max_length=200)
    #content = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

class Unit(models.Model):
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE,null=True, blank=True)
    ingrd_id = models.ForeignKey(Ingred, on_delete=models.CASCADE,null=True, blank=True)
    unit = models.CharField(max_length=100)

    def __str__(self):
        return self.unit

class Steps(models.Model):
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    num = models.IntegerField(default=0)
    contents = models.CharField(max_length=1000)
    #img
    def __str__(self):
        return self.contents