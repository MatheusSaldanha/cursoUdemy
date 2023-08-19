from django.urls import resolve, reverse

from recipes import views
from recipes.models import Recipe

from .test_recipe_base import RecipeTestBase


class RecipeCategoryTestView(RecipeTestBase):        
    def test_recipe_category_template_dont_load_recipes_not_published(self):
        '''Testing if is_published is False, dont show '''
        
        recipe = self.make_recipe(is_published=False)
        
        response = self.client.get(
            reverse(
                'recipes-recipe', kwargs={'id':recipe.category.id}  # type: ignore
                )
            ) 
        
        self.assertEqual(response.status_code, 404) 
       

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse("category-view", kwargs={"category_id": 1}))
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse("category-view", kwargs={"category_id": 10000})
        )

        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_loads_recipes(self):
        needed_title = 'Category'
        # Need a recipe for this test
        self.make_recipe(title=needed_title)

        response = self.client.get(reverse('category-view', args=(1,)))
        content = response.content.decode('utf-8')

        # Check if one recipe exists
        self.assertIn(needed_title, content)



