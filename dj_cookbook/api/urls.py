# from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from .views import (
    RecipeViewSet,
    RecipeViewSetQ,
    add_product_to_recipe,
    cook_recipe,
    show_recipes_without_product,
)

# UserViewSet, IngredientViewSet, RecipeViewSet,

router = routers.DefaultRouter()
# router.register("cook_recipe", cook_recipe, name='index')
router.register("add_product_to_recipe", RecipeViewSet, basename="recipes")
# router.register('show_recipes_without_product', SessionViewSet,
#                basename='session')

urlpatterns = [
    path("", include(router.urls)),
    path(
        "show_recipes_without_product/<product_id>/",
        show_recipes_without_product,
        name="show_recipes_without_product",
    ),
    path("cook_recipe/<recipe_id>/", cook_recipe, name="cook_recipe"),
    # path(
    #     "add_product_to_recipe/<recipe_id>,<product_id>,<weight>",
    #     add_product_to_recipe,
    #     name="add_product_to_recipe",
    # ),
]
