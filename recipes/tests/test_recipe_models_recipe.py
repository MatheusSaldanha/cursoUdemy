from django.core.exceptions import ValidationError
from parameterized import parameterized

from .test_recipe_base import Recipe, RecipeTestBase


class RecipeModelsTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()
    
    def test_recipe_title_rasises_error_if_title_has_more_than_65_char(self):
        self.recipe.title = 'A' * 70
        
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()
            
    def make_recipe_no_default(self):
         recipe= Recipe(
            category=self.make_category(name='this is a test'),
            author=self.make_author(username='Goriala03'),
            title="Recipe Title",
            description="Recipe Description",
            slug="recipe-slug-for-no-defaults",
            preparation_time=10,
            preparation_time_unit="Minutos",
            servings=5,
            servings_unit="Porções",
            preparation_steps="Recipe Preparation Steps",

        )
         recipe.full_clean()
         recipe.save()
         return recipe
    
    @parameterized.expand([
        ('title', 50),
        ('description', 165),
        ('preparation_time_unit', 50),
        ('servings_unit', 50)
    ])
    
    def test_recipe_fields_max_length(self, field, max_length):
        setattr(self.recipe, field , 'A' * (max_length + 1))
        
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()
            
    def test_recipe_preparation_steps_is_html_is_false_by_default(self):
        recipe= self.make_recipe_no_default()
        recipe.full_clean()
        recipe.save()
        self.assertFalse(recipe.preparation_steps_is_html)
        
    def test_recipe_is_published_is_false_by_default(self):
        recipe= self.make_recipe_no_default()
        recipe.full_clean()
        recipe.save()
        self.assertFalse(
            recipe.is_published,
            msg="is_published is not False"
        )
    def test_recipe_string_representation(self):
        self.recipe.title = 'Test Representations'
        self.recipe.full_clean()
        self.recipe.save()
        
        self.assertEqual(str(self.recipe), 'Test Representations')