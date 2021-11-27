from django.urls import path, include
from .views import *

urlpatterns = [
    # path('', RecipeView.as_view()),
    # path('<int:recipe_id>', RecipeView.as_view()),

    path('add/', RecipeCreateAPI.as_view()),
    path('<int:id>/', RecipeDetails.as_view()),
    path('list/<int:id>/', RecipeListViewAPI.as_view()),
    path('list/', RecipeListViewAPI.as_view()),

    path('steps/add/', StepsCreateAPI.as_view()),
    path('steps/<int:id>/', StepsAPI.as_view()),
    path('steps/all/<int:id>/', StepsAllViewAPI.as_view()),

    path('unit/add/', UnitCreateAPI.as_view()),
    path('unit/<int:id>/', UnitAPI.as_view()),
    path('unit/all/<int:id>/', UnitAllViewAPI.as_view())

]