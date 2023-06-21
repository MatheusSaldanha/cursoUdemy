from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render

from utils.recipes.factory import make_recipe

from .models import Recipe


def home(request):
    recipe = Recipe.objects.filter(is_published=True).order_by("-id")
    return render(
        request,
        "recipes/pages/home.html",
        {"recipes": recipe},
    )


def category(request, category_id):
    recipe = Recipe.objects.filter(
        category__id=category_id, is_published=True
    ).order_by("-id")

    if not recipe:
        raise Http404("Not Found 🥲")

    return render(
        request,
        "recipes/pages/category.html",
        context={
            "recipes": recipe,
            "title": f"{recipe.first().category.name} - Category | ",
        },
    )


def recipe(request, id):
    recipe = Recipe.objects.filter(recipe__id=id)
    return render(
        request,
        "recipes/pages/recipes-view.html",
        context={"recipe": recipe},
    )
