from .test_recipe_base import RecipeTestBase
from django.core.exceptions import ValidationError
from parameterized import parameterized


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    # title = models.CharField(max_length=65)
    # description = models.CharField(max_length=165)
    # preparation_time_unit = models.CharField(max_length=65)
    # servings_unit = models.CharField(max_length=65)
    @parameterized.expand([
        ('title', 65),
        ('description', 165),
        ('preparation_time_unit', 65),
        ('servings_unit', 65),
    ])
    def test_recipe_fields_max_length(self, field, max_length):
        setattr(self.recipe, field, "C" * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    # slug = models.SlugField()

    # preparation_time = models.IntegerField()

    # servings = models.IntegerField()

    # preparation_steps = models.TextField()

    # preparation_steps_is_html = models.BooleanField(default=False)

    # created_at = models.DateTimeField(auto_now_add=True)

    # updated_at = models.DateTimeField(auto_now=True)

    # is_published = models.BooleanField(default=False)
