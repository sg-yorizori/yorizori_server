from django.db import models

class Ingred(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    title = models.CharField(max_length=100)
    main_img = models.CharField(max_length=500)
    ingreds = models.ManyToManyField(Ingred)
    ingred_amount = models.CharField(max_length=500)
    steps = models.CharField(max_length=500)
    step_img = models.CharField(max_length=500)
    views = models.IntegerField(default=0)
    writer = models.CharField(max_length=50)

    def __str__(self):
        return self.title


