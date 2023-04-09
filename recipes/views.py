from django.shortcuts import render, get_object_or_404
from .models import Recipe


def home(request):
    recipes = Recipe.objects.filter(
        is_published=True,
    ).order_by('-id')
    return render(request, 'recipes/pages/home.html', context={
        'recipes': recipes,
        'is_home_page': True,
    })


def category(request, category_id):
    recipes = Recipe.objects.filter(
        category__id=category_id,
        is_published=True,
    ).order_by('-id')
    return render(request, 'recipes/pages/category.html', context={
        'recipes': recipes,
        'is_home_page': True,
    })


def recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': recipe,
    })
