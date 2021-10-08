from rest_framework import serializers
from .models import Recipe, Ingred

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'title', 'main_img', 'ingreds', 'ingred_amount', 'steps',
                  'step_img', 'views', 'writer')

class IngredSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingred
        fields = ('id', 'name')