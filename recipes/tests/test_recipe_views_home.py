from django.urls import resolve, reverse
from .test_recipe_base import RecipeTestBase
from recipes import views
from unittest.mock import patch


class RecipeViewsHomeTest(RecipeTestBase):
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func.view_class, views.RecipeListViewHome)

    def test_recipe_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_returns_correct_template(self):
        template = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(template, "recipes/pages/home.html")

    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        content = self.client.get(reverse('recipes:home'))
        self.assertIn(
            "Recipes not found",
            content.content.decode('utf-8'))

    def test_recipe_home_template_loads_recipes(self):
        self.make_recipe()
        # Need a recipe for this test
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']
        # Check if the recipe exists and if the codes print correctly
        self.assertIn("Recipe Title Test", content)
        self.assertEqual(len(response_context_recipes), 1)

    def test_recipe_home_template_not_loads_recipes_not_published(self):
        self.make_recipe(is_published=False)
        """Test if the recipes with is_published=False is not loaded"""
        # Need a recipe for this test
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        # Check if the the return in the page is recipes not found
        self.assertIn("Recipes not found", content)

    @patch('recipes.views.PER_PAGE', 3)
    def test_recipe_home_is_paginated(self):
        self.make_recipe_in_batch(8)

        response = self.client.get(reverse('recipes:home'))
        recipes = response.context['recipes']
        paginator = recipes.paginator

        self.assertEqual(paginator.num_pages, 3)
        self.assertEqual(len(paginator.get_page(1)), 3)
        self.assertEqual(len(paginator.get_page(2)), 3)
        self.assertEqual(len(paginator.get_page(3)), 2)

    @patch('recipes.views.PER_PAGE', 3)
    def test_invalid_page_query_uses_page_one(self):
        self.make_recipe_in_batch(8)

        # test paginator returns page 1
        response = self.client.get(reverse('recipes:home') + '?page=1TEST')
        paginator = response.context['recipes'].number
        self.assertEqual(paginator, 1)
        # test paginator returns page 2 instead 1
        response = self.client.get(reverse('recipes:home') + '?page=2')
        paginator = response.context['recipes'].number
        self.assertNotEqual(paginator, 1)
