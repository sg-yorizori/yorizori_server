from django.urls import path, include
from .views import *

urlpatterns = [
    path("", RecipeView.as_view()),
]