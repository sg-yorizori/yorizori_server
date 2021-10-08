from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render, get_object_or_404
from .models import Recipe, Ingred
from .serializers import RecipeSerializer, IngredSerializer

class RecipeView(APIView):
    def get(self, request, **kwargs):
        if kwargs.get('recipe_id') is None:
            recipe_serializer = RecipeSerializer(
                Recipe.objects.all(), many=True)
            return Response(recipe_serializer.data, status=200)
        else:
            recipe_id = kwargs.get('recipe_id')
            recipe_serializer = RecipeSerializer(
                get_object_or_404(Recipe, id=recipe_id))
            return Response(recipe_serializer.data, status=200)

class IngredView(APIView):
    def get(self, request, **kwargs):
        if kwargs.get('ingred_id') is None:
            ingred_serializer = IngredSerializer(
                Ingred.objects.all(), many=True)
            return Response(ingred_serializer.data, status=200)
        else:
            ingred_id = kwargs.get('ingred_id')
            ingred_serializer = IngredSerializer(
                get_object_or_404(Ingred, id=ingred_id))
            return Response(ingred_serializer.data, status=200)
