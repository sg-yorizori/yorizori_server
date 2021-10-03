from django.db import models

class Recipe(models.Model):
    title = models.CharField(max_length=100)
    ingredients = models.CharField(max_length=200)
    writer = models.CharField(max_length=50)
