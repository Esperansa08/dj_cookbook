# from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from .views import (IngredientViewSet, RecipeViewSet,
                    show_recipes_without_product)  # UserViewSet

router = routers.DefaultRouter()
router.register("cook_recipe", IngredientViewSet, basename="ingredients")
router.register("add_product_to_recipe", RecipeViewSet, basename="recipes")
# router.register('show_recipes_without_product', SessionViewSet,
#                basename='session')

urlpatterns = [
    path(
        "",
        include(
            router.urls)),
    path(
        "show_recipes_without_product/",
        show_recipes_without_product,
        name="show_recipes_without_product"),
]
