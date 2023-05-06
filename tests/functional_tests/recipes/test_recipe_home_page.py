from selenium.webdriver.common.by import By
import pytest
from tests.functional_tests.recipes.base import RecipeBaseFunctionalTest
from unittest.mock import patch


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    def test_recipe_home_page_without_recipes_show_not_found_recipes(self):
        browser = self.browser
        browser.get(self.live_server_url)
        body = browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('Recipes not found... 😢', body.text)

    def test_the_developer(self):
        browser = self.browser
        browser.get(self.live_server_url)
        body = browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('Well Jackson', body.text)

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipes_appear(self):
        self.make_recipe_in_batch()
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('Recipe Title Test', body.text)
