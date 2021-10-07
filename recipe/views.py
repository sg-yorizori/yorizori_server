from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render, get_object_or_404
from .models import Recipe, Ingred
from .serializers import RecipeSerializer

'''
def recipeAPI(request):
    all_recipe = Recipe.objects.all()
    serializer = RecipeSerializer(all_recipe, many=True)
    return Response(serializer.data)
'''
class RecipeView(APIView):
    def get(self, request, **kwargs):
        if kwargs.get('profile_id') is None:
            recipe_serializer = RecipeSerializer(
                Recipe.objects.all(), many=True)
            # user 전체 리스트 get
            return Response(recipe_serializer.data, status=200)
        else:
            recipe_id = kwargs.get('profile_id')
            recipe_serializer = RecipeSerializer(
                get_object_or_404(Recipe, id=recipe_id))
            return Response(recipe_serializer.data, status=200)