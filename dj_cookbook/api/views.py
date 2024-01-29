from django.contrib.auth import get_user_model

# from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

# from django_filters.rest_framework import DjangoFilterBackend
# from djoser.views import UserViewSet
from rest_framework import filters, status, viewsets
from rest_framework.decorators import api_view  # , renderer_classes
from rest_framework.response import Response

# from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from .models import Ingredient, Recipe  # IngredientInRecipe

# from .filters import RecipeFilter
from .serializers import IngredientSerializer, RecipeSerializer

User = get_user_model()


# class UserViewSet(viewsets.ModelViewSet):#UserViewSet):
#     serializer_class = CustomUserSerializer
#     queryset = User.objects.all()
#    # pagination_class = CustomPagination
#     filter_backends = (filters.SearchFilter,)
#     search_fields = ('username',)


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

    # def get_serializer_class(self):
    #     if self.request.method == 'GET':
    #         return RecipeSerializerRead
    #     return RecipeSerializerWrite

    # def get_queryset(self):
    #     queryset = Recipe.objects.all()
    #     return queryset

    def add_recipe(self, model, user, pk):
        if model.objects.filter(user=user, recipe__id=pk).exists():
            return Response({"errors": "Рецепт уже добавлен!"},
                            status=status.HTTP_400_BAD_REQUEST)
        recipe = get_object_or_404(Recipe, id=pk)
        model.objects.create(user=user, recipe=recipe)
        serializer = RecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_recipe(self, model, user, pk):
        recipe_del = model.objects.filter(user=user, recipe__id=pk)
        if recipe_del.exists():
            recipe_del.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"errors": "Рецепт уже удален!"},
                        status=status.HTTP_400_BAD_REQUEST)


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
def add_product_to_recipe(request, recipe_id, product_id, weight):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    ingredient = Ingredient.objects.get(recipes__id=recipe.id, id=product_id)
    if ingredient:
        ingredient.amount = weight
        print(ingredient)
        ingredient.save(update_fields=["amount"])
    serializer = RecipeSerializer(recipe)
    return Response(serializer.data, status=status.HTTP_200_OK)
