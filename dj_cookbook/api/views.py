from itertools import chain

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view

from .models import Ingredient, IngredientInRecipe, Recipe

User = get_user_model()


@api_view(("GET",))
def cook_recipe(request, recipe_id):
    """Увеличение на единицу количества приготовленных блюд для каждого
    продукта, входящего в указанный рецепт"""
    recipe = get_object_or_404(Recipe, id=recipe_id)
    ingredients = Ingredient.objects.filter(recipes__id=recipe.id)
    for ingredient in ingredients:
        ingredient.cooked_times += 1
        ingredient.save(update_fields=["cooked_times"])
    return HttpResponse(
        f"""В рецепте {recipe} увеличено на 1 количества
                        приготовленных блюд из: {list(({ingredient.name},
                {ingredient.cooked_times}) for ingredient in ingredients)}"""
    )


@api_view(("GET",))
def show_recipes_without_product(request, product_id):
    """возвращает HTML страницу, на которой размещена таблица.
    В таблице отображены id и названия всех рецептов, в которых указанный
    продукт отсутствует, или присутствует в количестве меньше 10 грамм"""
    recipes_without_id = Recipe.objects.exclude(ingredients__id=product_id)
    recipes_lte = Recipe.objects.filter(
        ingredients__id=product_id, ingredient_list__amount__lte=10)
    context = {"recipes": list(chain(recipes_without_id, recipes_lte))}
    return render(request, "base.html", context)


@api_view(("GET",))
def add_product_to_recipe(request):
    """Добавение к рецепту продукт с указанным весом"""
    recipe_id = request.GET.get("recipe_id")
    product_id = request.GET.get("product_id")
    weight = request.GET.get("weight")
    recipe = get_object_or_404(Recipe, id=recipe_id)

    ingredient = IngredientInRecipe.objects.get_or_create(
        recipe_id=recipe.id, ingredient_id=product_id, amount=weight
    )
    return HttpResponse(f"""У рецепта {recipe} ингредиент {ingredient[0]}""")
