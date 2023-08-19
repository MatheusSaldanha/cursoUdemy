from django.core.exceptions import ValidationError

from .test_recipe_base import RecipeTestBase


class RecipeCategoryModelsTest(RecipeTestBase):
    def setUp(self) -> None:
        self.categoty = self.make_category(
            name='Category Testing'
        )
        return super().setUp()
    
    def test_recipe_category_string_represetation(self):
        self.assertEqual(
            str(self.categoty),
            self.categoty.name
        )
    def test_recipe_category_name_max_length_is_65_chars(self):
        self.categoty.name = 'a' * 51
        
        with self.assertRaises(ValidationError):
            self.categoty.full_clean()
    
    