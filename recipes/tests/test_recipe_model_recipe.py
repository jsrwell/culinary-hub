from .test_recipe_base import RecipeTestBase
from django.core.exceptions import ValidationError


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def test_recipe_title_erro_if_more_than_65_chars(self):
        self.recipe.title = "C" * 66
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()
