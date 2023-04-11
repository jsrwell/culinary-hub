from django.test import TestCase
from django.urls import reverse


class RecipeURLsTest(TestCase):
    def test_the_pytest_is_ok(self):
        assert 1 == 1, 'one is one'

    def test_recipe_home_home_url_is_correct(self):
        home_url = reverse('recipes:home')
        self.assertEqual(home_url, "/")
