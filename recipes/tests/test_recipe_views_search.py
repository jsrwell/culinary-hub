from django.urls import resolve, reverse
from .test_recipe_base import RecipeTestBase
from recipes import views


class RecipeViewsSearchTest(RecipeTestBase):
    def test_recipe_search_view_function_is_correct(self):
        view = resolve(reverse('recipes:search'))
        self.assertIs(view.func.view_class, views.RecipeListViewSearch)

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

    def test_recipe_search_can_find_recipe_by_title(self):
        title1 = 'Titulo 1'
        title2 = 'Titulo 2'
        recipe1 = self.make_recipe(
            slug='one', title=title1, author_data={'username': 'one'}
        )
        recipe2 = self.make_recipe(
            slug='two', title=title2, author_data={'username': 'two'}
        )
        search_url = reverse('recipes:search')
        response1 = self.client.get(f'{search_url}?q={title1}')
        response2 = self.client.get(f'{search_url}?q={title2}')
        response_both = self.client.get(f'{search_url}?q=Titulo')
        self.assertIn(recipe1, response1.context['recipes'])
        self.assertNotIn(recipe2, response1.context['recipes'])
        self.assertIn(recipe2, response2.context['recipes'])
        self.assertNotIn(recipe1, response2.context['recipes'])
        self.assertIn(recipe1, response_both.context['recipes'])
        self.assertIn(recipe2, response_both.context['recipes'])
