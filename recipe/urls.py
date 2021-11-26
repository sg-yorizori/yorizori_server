from django.urls import path, include
from .views import *

urlpatterns = [
    # path('', RecipeView.as_view()),
    # path('<int:recipe_id>', RecipeView.as_view()),

    path('', RecipeAPIView.as_view()),
    path('all/', RecipeAPIView.as_view()),
    path('detail/<int:id>/', RecipeDetails.as_view()),

    path('ingred/', IngredView.as_view()),
    path('ingred/<int:ingred_id>', IngredView.as_view())
]