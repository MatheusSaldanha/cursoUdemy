from django.urls import path

from . import views

# app_name = "recipes"

urlpatterns = [
    path("", views.home, name="recipes-home"),
    path("recipes/search/", views.search, name="recipes-search"),
    path(
        "recipes/category/<int:category_id>/", views.category, name="category-view"
    ),  # flake8: noqa
    path("recipes/<int:id>/", views.recipe, name="recipes-recipe"),
    
]
