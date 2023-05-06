from typing import KeysView
from selenium.webdriver.common.by import By
import pytest
from tests.functional_tests.recipes.base import RecipeBaseFunctionalTest
from unittest.mock import patch
from selenium.webdriver.common.keys import Keys


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

    def test_recipes_appear(self):
        self.make_recipe_in_batch()
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('Recipe Title Test 3', body.text)

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_search_input_can_find_correct_recipes(self):
        recipes = self.make_recipe_in_batch()
        title_to_search = 'This is what I need'
        recipes[0].title = title_to_search
        recipes[0].save()

        # User open the page
        self.browser.get(self.live_server_url)

        # The user see the field "search"
        search_input = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="Search for a recipe"]')

        # Click, type and press enter to search the term
        search_input.send_keys(title_to_search)
        search_input.send_keys(Keys.ENTER)

        # The user find the recipe he wants
        self.assertIn(
            title_to_search,
            self.browser.find_element(
                By.CLASS_NAME, 'main-content-list'
            ).text
        )
