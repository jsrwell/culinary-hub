from selenium.webdriver.common.by import By
from tests.functional_tests.recipes.base import RecipeBaseFunctionalTest


class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    def test_recipe_home_page_without_recipes_show_not_found_recipes(self):
        browser = self.browser
        browser.get(self.live_server_url)
        body = browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('Recipes not found... 😢', body.text)

    def test_the_developer(self):
        browser = self.browser
        browser.get(self.live_server_url)
        # self.sleep()
        body = browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('Well Jackson', body.text)
