from django.contrib.auth import get_user_model

# from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

# from django_filters.rest_framework import DjangoFilterBackend
# from djoser.views import UserViewSet
from rest_framework import filters, status, viewsets
from rest_framework.decorators import api_view  # , renderer_classes
from rest_framework.response import Response

# from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from .models import Ingredient, IngredientInRecipe, Recipe

# from .filters import RecipeFilter
from .serializers import (  # RecipesSerializer,
    IngredientInRecipeSerializer,
    IngredientSerializer,
    RecipeSerializer,
    RecipeSerializerRead,
    RecipeSerializerWrite,
    RecipesSerializer1,
)

User = get_user_model()


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("^name",)
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    # pagination_class = CustomPagination
    # filterset_class = RecipeFilter
    # filter_backends = (DjangoFilterBackend,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializerRead
            # return RecipeSerializerWrite

    def get_queryset(self):
        queryset = Recipe.objects.all()
        return queryset


@api_view(("GET",))
def cook_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    ingredients = Ingredient.objects.filter(recipes__id=recipe.id)
    for ingredient in ingredients:
        ingredient.cooked_times += 1
        ingredient.save(update_fields=["cooked_times"])
    serializer = RecipeSerializer(recipe)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(("GET",))
def show_recipes_without_product(request, product_id):
    recipes = Recipe.objects.filter(ingredients__id=product_id,
                                    ingredient_list__amount__lte=10)
    context = {"recipes": recipes}
    return render(request, "base.html", context)


@api_view(("GET",))
def add_product_to_recipe(request, recipe_id):  # , product_id, weight):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    ingredient = IngredientInRecipe.objects.get(recipe_id=recipe.id,
                                                id=product_id)
    if ingredient:
        ingredient.amount = weight
        print(ingredient)
        ingredient.save(update_fields=["amount"])
    serializer = IngredientInRecipeSerializer(ingredient)
    return Response(serializer.data, status=status.HTTP_200_OK)


class RecipeViewSetQ(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipesSerializer1

    # def get(self, request):
    #     print('!!!!', request)
    #     w = Recipe.objects.all()
    #     return Response({'posts': RecipesSerializer1(w, many=True).data})


class RecipeViewSet(viewsets.ModelViewSet):
    # permission_classes = IsAuthorModeratorAdminOrReadOnly,
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def get_recipe(self):
        recipe_id = self.kwargs.get("recipe_id")
        if not Recipe.objects.filter(pk=recipe_id).exists():
            raise Exception(
                detail='Не найден рецепт',
                code=status.HTTP_404_NOT_FOUND)
        return Recipe.objects.get(pk=recipe_id)

    def perform_create(self, serializer):
        self.get_title()
        recipe = self.get_recipe()
        serializer.save(
            recipe=recipe)

    def perform_update(self, serializer):
        self.get_title()
        recipe = self.get_recipe()
        serializer.save(recipe=recipe)
