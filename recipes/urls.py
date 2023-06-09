from django.urls import path
from . import views

app_name = "recipes"

urlpatterns = [
    path(
        '',
        views.RecipeListViewHome.as_view(),
        name="home"
    ),
    path(
        'recipes/search/',
        views.RecipeListViewSearch.as_view(),
        name="search"
    ),
    path(
        'recipes/<int:pk>/',
        views.RecipeDetail.as_view(),
        name="recipe"
    ),
    path(
        'recipes/category/<int:category_id>/',
        views.RecipeListViewCategory.as_view(),
        name="category"
    ),
    path(
        'recipes/api/v1/',
        views.RecipeListViewHomeApi.as_view(),
        name="recipes_api_v1",
    ),
]
