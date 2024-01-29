from django.contrib import admin

from .models import Ingredient, IngredientInRecipe, Recipe


class IngredientsInline(admin.TabularInline):
    model = IngredientInRecipe
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )
    search_fields = ("name",)
    exclude = [
        "ingredients",
    ]


@admin.register(Ingredient)
class IngredienteAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "measurement_unit", "cooked_times")
    list_filter = ("name",)
    search_fields = ("name",)


@admin.register(IngredientInRecipe)
class IngredientInRecipeAdmin(admin.ModelAdmin):
    list_display = ("ingredient", "recipe_id", "recipe", "amount")
    ordering = ("-recipe_id",)
    search_fields = ("ingredient",)
    list_filter = ("recipe",)
