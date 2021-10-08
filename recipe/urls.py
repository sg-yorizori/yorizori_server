from django.urls import path, include
from .views import *

urlpatterns = [
    path('', RecipeView.as_view()),
    path('<int:recipe_id>', RecipeView.as_view()),

    path('ingred/', IngredView.as_view()),
    path('ingred/<int:ingred_id>', IngredView.as_view())
]