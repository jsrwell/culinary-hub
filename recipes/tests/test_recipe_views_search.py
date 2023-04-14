from django.urls import resolve, reverse
from .test_recipe_base import RecipeTestBase
from recipes import views


class RecipeViewsSearchTest(RecipeTestBase):
    def test_recipe_search_view_function_is_correct(self):
        view = resolve(reverse('recipes:search'))
        self.assertIs(view.func, views.search)

    def test_recipe_search_loads_correct_template(self):
        search_term = 'teste'
        url = reverse('recipes:search') + '?q=' + search_term
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_recipe_search_raises_404_if_no_search_term(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_is_on_the_title_and_escaped(self):
        search_term = 'teste'
        url = reverse('recipes:search') + '?q=' + search_term
        response = self.client.get(url)
        self.assertIn(
            f'Search for &quot;{search_term}&quot;',
            response.content.decode('utf-8'),
        )
