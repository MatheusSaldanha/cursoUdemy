from django.urls import resolve, reverse

from recipes import views
from recipes.models import Recipe
from unittest.mock import patch
from .test_recipe_base import RecipeTestBase


class RecipeHomeTestView(RecipeTestBase):
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
    


    def test_recipe_home_is_paginated(self):
        for i in range(8):
            kwargs = {'slug': f'r{i}', 'author_data': {'username': f'u{i}'}}
            self.make_recipe(**kwargs)

        with patch('recipes.views.PER_PAGE', new=3):
            response = self.client.get(reverse('recipes:home'))
            recipes = response.context['recipes']
            paginator = recipes.paginator

            self.assertEqual(paginator.num_pages, 3)
            self.assertEqual(len(paginator.get_page(1)), 3)
            self.assertEqual(len(paginator.get_page(2)), 3)
            self.assertEqual(len(paginator.get_page(3)), 2)            