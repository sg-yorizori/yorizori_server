from rest_framework import serializers
from .models import Recipe, Ingred


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'
        # Profile의 모든 field를 serializer함.

class RecipeCRSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ("writer", "title", "created_date")
        # Profile의 모든 field를 serializer함.

class IngredSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingred
        fields = '__all__'
