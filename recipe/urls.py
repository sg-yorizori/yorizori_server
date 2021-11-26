from django.urls import path, include
from .views import *

urlpatterns = [
    # path('', RecipeView.as_view()),
    # path('<int:recipe_id>', RecipeView.as_view()),

    path('add/', RecipeAPIView.as_view()),
    path('all/<int:id>/', RecipeAPIView.as_view()),
    path('detail/<int:id>/', RecipeDetails.as_view()),

    path('steps/add/', StepsCreateAPI.as_view()),
    path('steps/<int:id>/', StepsAPI.as_view()),
    path('steps/all/<int:id>/', StepsAllViewAPI.as_view())

]