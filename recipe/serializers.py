from rest_framework import serializers
from .models import Recipe, Steps, Unit, Ingredients


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'
        # Profile의 모든 field를 serializer함.

class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Steps
        fields = '__all__'

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'

class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = '__all__'
