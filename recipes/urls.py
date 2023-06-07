from django.urls import path
from . import views

app_name = "recipes"

urlpatterns = [
    path('', views.RecipeListViewBase.as_view(), name="home"),
    path('recipes/search/', views.search, name="search"),
    path('recipes/<int:id>/', views.recipe, name="recipe"),
    path('recipes/category/<int:category_id>/',
         views.category, name="category"),
]
