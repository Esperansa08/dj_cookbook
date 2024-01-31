from django.urls import path

from .views import (
    add_product_to_recipe,
    cook_recipe,
    show_recipes_without_product,
)

urlpatterns = [
    path(
        "show_recipes_without_product/<product_id>/",
        show_recipes_without_product,
        name="show_recipes_without_product",
    ),
    path("cook_recipe/<recipe_id>/", cook_recipe, name="cook_recipe"),
    path(
        "add_product_to_recipe/",
        add_product_to_recipe,
        name="add_product_to_recipe",
    ),
]
