from .test_recipe_base import RecipeTestBase
from django.core.exceptions import ValidationError


class CateogoryModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.category = self.make_category(
            name='Category Testing'
        )
        return super().setUp()

    # Class Category def __str__(self):
    def test_category_string_representation(self):
        testword = 'Name Representation'
        self.category.name = testword
        self.category.full_clean()
        self.category.save()
        self.assertEqual(str(self.category), testword,
                         msg=f'Category string must be "{testword}"')

    # name = models.CharField(max_length=65)
    def test_recipe_category_model_max_length_is_65_chars(self):
        self.category.name = 'C' * 66
        with self.assertRaises(ValidationError):
            self.category.full_clean()
