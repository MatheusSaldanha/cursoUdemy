from django.urls import resolve, reverse

from recipes import views
from recipes.models import Recipe

from .test_recipe_base import RecipeTestBase


class RecipeViewTest(RecipeTestBase):
    def test_recipe_home_views_function_is_correct(self):
        view = resolve(reverse("recipes-home"))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse("recipes-home"))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_template_shows_no_recipes_found_if_no_correct(self):
        response = self.client.get(reverse("recipes-home"))
        self.assertIn(
            "<h1>There is not recipes here 🥲</h1>", response.content.decode("utf-8")
        )

    def test_recipe_home_view_returns_loads_correct_template(self):
        response = self.client.get(reverse("recipes-home"))
        self.assertTemplateUsed(response, "recipes/pages/home.html")

    # teste que verifica se as receitas estão sendo exibidas no template
    def test_recipe_home_template_loads_recipes(self):
        self.make_recipe(author_DATA={"first_name": "Matheus"})

        response = self.client.get(
            reverse("recipes-home")
        )  # recebendo o template usado no teste

        # content testa se o conteudo esta no html
        content = response.content.decode("utf-8")

        # teste sendo feito para verificar se as recipes existem
        self.assertIn("Recipe Title", content)
        self.assertIn("Matheus", content)
        
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

    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse("recipes-recipe", kwargs={"id": 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(reverse("recipes-recipe", kwargs={"id": 1}))

        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_loads_the_correct_recipes(self):
        needed_title = 'This is a detail page - It load  one recipe'
        # Need a recipe for this test
        self.make_recipe(title=needed_title)

        response = self.client.get(
            reverse(
                'recipes-recipe', 
                kwargs={
                    'id':1
                    }
                )
            )
        content = response.content.decode('utf-8')

        # Check if one recipe exists
        self.assertIn(needed_title, content)
        
    def test_recipe_detail_template_dont_load_recipes_not_published(self):
        '''testing if is_published is False, don't show '''
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(
            reverse('recipes-recipe', kwargs={'id':recipe.id}) # type: ignore
        )
        
        self.assertEqual(response.status_code, 404)
        
    def test_recipe_search_users_correct_view_function(self):
        url = reverse("recipes-search")
        resolved = resolve(url)
        self.assertIs(resolved.func, views.search)
        
    def test_recipe_search_loads_correct_template(self):
        response = self.client.get(reverse("recipes-search")+ '?q=teste')
        self.assertTemplateUsed(response, "recipes/pages/search.html")

    def test_recipe_search_raises_404_if_no_search_term(self):
        response = self.client.get(reverse("recipes-search"))
        self.assertEquals(response.status_code, 404)
        
    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        url = reverse("recipes-search") + '?q=Teste'
        response = self.client.get(url)
        
        self.assertIn(
            'Serach for &quot;Teste&quot;',
            response.content.decode('utf-8')
        )