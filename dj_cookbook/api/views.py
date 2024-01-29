from django.contrib.auth import get_user_model
# from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

# from django_filters.rest_framework import DjangoFilterBackend
# from djoser.views import UserViewSet
from rest_framework import filters, status, viewsets
from rest_framework.response import Response

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

    def cook_recipe(self, model, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        model.objects.create(recipe=recipe)
        # model.objects.
        serializer = RecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# class SessionViewSet(viewsets.ViewSet):
#     queryset = Recipe.objects.all()
#     serializer_class = RecipeSerializer


def show_recipes_without_product(request):  # , product_id):
    recipes = Recipe.objects.filter(
        ingredients__id=1).filter(
        ingredient_list__amount=10)
    context = {
        "recipes": recipes,
    }
    return render(request, "base.html", context)
