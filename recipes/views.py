import os
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, get_list_or_404, get_object_or_404
from .models import Recipe
from utils.pagination import make_pagination

PER_PAGES = int(os.environ.get('PER_PAGES', 9))
PAGINATOR_SIZE = int(os.environ.get('PAGINATOR_SIZE', 3))


def home(request):
    recipes = Recipe.objects.filter(
        is_published=True,
    ).order_by('-id')

    page_obj, pagination_range = make_pagination(
        request, recipes, PER_PAGES, PAGINATOR_SIZE)

    return render(request, 'recipes/pages/home.html', context={
        'recipes': page_obj,
        'pagination_range': pagination_range,
        'is_home_page': True,
    })


def category(request, category_id):
    recipes = get_list_or_404(
        Recipe.objects.filter(
            category__id=category_id,
            is_published=True,
        ).order_by('-id')
    )

    page_obj, pagination_range = make_pagination(
        request, recipes, PER_PAGES, PAGINATOR_SIZE)

    return render(request, 'recipes/pages/category.html', context={
        'recipes': page_obj,
        'pagination_range': pagination_range,
        'title': recipes[0].category.name,
        'is_home_page': True,
    })


def recipe(request, id):
    recipe = get_object_or_404(Recipe, pk=id, is_published=True)
    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': recipe,
    })


def search(request):
    search_term = request.GET.get('q', '').strip()
    if not search_term:
        raise Http404()
    recipes = Recipe.objects.filter(
        Q(title__icontains=search_term) | Q(
            description__icontains=search_term),
        is_published=True,
    ).order_by('-id')

    page_obj, pagination_range = make_pagination(
        request, recipes, PER_PAGES, PAGINATOR_SIZE)

    return render(request, 'recipes/pages/search.html', {
        'page_title': f'Search for "{search_term}"',
        'search_term': search_term,
        'recipes': page_obj,
        'pagination_range': pagination_range,
        'additional_url_query': f'&q={search_term}',
        'is_home_page': True,
    })
