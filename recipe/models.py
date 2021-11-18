from django.db import models

class Ingred(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    title = models.CharField(max_length=100)
    ingredients = models.CharField(max_length=200)
    writer = models.CharField(max_length=50)
    content = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


