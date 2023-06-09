from django.urls import resolve, reverse
from .test_recipe_base import RecipeTestBase
from recipes import views


class RecipeViewsCategoryTest(RecipeTestBase):
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func.view_class, views.RecipeListViewCategory)

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
