from django.urls import resolve, reverse
from .test_recipe_base import RecipeTestBase
from recipes import views


class RecipeViewsTest(RecipeTestBase):

    # HOME tests ///////////////////////////////////////////////////////
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

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
            content.content.decode('utf-8'),
        )

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

    # CATEGORY Tests ////////////////////////////////////////////////////////
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_returns_status_code_200_OK(self):
        self.make_recipe()
        # Need a recipe for this test
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertEqual(response.status_code, 200)

    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 9999}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_loads_recipes(self):
        title_test = "This is a category test"
        self.make_recipe(title=title_test)
        # Need a recipe for this test
        response = self.client.get(
            reverse('recipes:category', args=(1,)
                    ))
        content = response.content.decode('utf-8')
        self.assertIn(title_test, content)

    def test_recipe_category_template_not_loads_recipes_not_published(self):
        self.make_recipe(is_published=False)
        """Test if the recipes with is_published=False is not loaded"""
        # Need a recipe for this test
        response = self.client.get(reverse(
            'recipes:category', kwargs={"category_id": 1}
        ))
        self.assertEqual(response.status_code, 404)

    # DETAILS Tests ///////////////////////////////////////////////////////
    def test_recipe_details_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_details_view_returns_status_code_200_OK(self):
        self.make_recipe()
        # Need a recipe for this test
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 200)

    def test_recipe_details_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 9999}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_details_template_loads_recipes(self):
        title_test = "This is a recipe test"
        self.make_recipe(title=title_test)
        # Need a recipe for this test
        response = self.client.get(
            reverse('recipes:recipe', args=(1,)))
        content = response.content.decode('utf-8')
        self.assertIn(title_test, content)

    def test_recipe_details_template_not_loads_recipes_not_published(self):
        self.make_recipe(is_published=False)
        """Test if the recipes with is_published=False is not loaded"""
        # Need a recipe for this test
        response = self.client.get(reverse(
            'recipes:recipe', kwargs={"id": 1}
        ))
        self.assertEqual(response.status_code, 404)

    # SEARCH Tests ///////////////////////////////////////////////////////

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
