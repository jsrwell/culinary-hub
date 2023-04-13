from .test_recipe_base import RecipeTestBase, Recipe
from django.core.exceptions import ValidationError
from parameterized import parameterized


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def make_recipe_with_defaults(self):
        recipe = Recipe(
            category=self.make_category(name='Test Default Category'),
            author=self.make_author(username='newuser'),
            title='Recipe Title Default',
            description='Recipe Description Default',
            slug='recipe-slug-Default',
            preparation_time=10,
            preparation_time_unit='Minutos Default',
            servings=5,
            servings_unit='Porções Default',
            preparation_steps='Recipe Preparation Steps Default',
        )
        recipe.full_clean()
        recipe.save()
        return recipe

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

    # preparation_steps_is_html = models.BooleanField(default=False)
    def test_recipe_preparation_steps_is_html_is_false_by_default(self):
        recipe = self.make_recipe_with_defaults()
        self.assertFalse(recipe.preparation_steps_is_html,
                         msg='Recipe preparation_status_is_html is not False'
                         )

    # is_published = models.BooleanField(default=False)
    def test_recipe_is_published_is_false_by_default(self):
        recipe = self.make_recipe_with_defaults()
        self.assertFalse(recipe.is_published,
                         msg='Recipe is_published is not False'
                         )

    # slug = models.SlugField()

    # preparation_time = models.IntegerField()

    # servings = models.IntegerField()

    # preparation_steps = models.TextField()

    # Class Recipe def __str__(self):
    def test_recipe_string_representation(self):
        testword = 'Testing Representation'
        self.recipe.title = testword
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(str(self.recipe), testword,
                         msg=f'Recipe string must be "{testword}"')
