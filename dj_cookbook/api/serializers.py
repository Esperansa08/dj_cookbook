from django.contrib.auth import get_user_model
# from django.core import validators
from django.db.models import F

# from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers  # , status
from rest_framework.exceptions import ValidationError
from rest_framework.fields import IntegerField
# from rest_framework.relations import PrimaryKeyRelatedField
# from rest_framework.validators import UniqueValidator

from .models import Ingredient, IngredientInRecipe, Recipe
# from .utils import clean_unique

User = get_user_model()


class CustomUserCreateSerializer(
        serializers.ModelSerializer):  # UserCreateSerializer):
    class Meta:
        fields = ("email", "username", "first_name", "last_name", "password")

        model = User


class CustomUserSerializer(serializers.ModelSerializer):  # UserSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed")
        model = User


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ("id", "name", "measurement_unit", "cooked_times")


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ("id", "name")


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = IntegerField(write_only=True)

    class Meta:
        model = IngredientInRecipe
        fields = ("id", "amount")


class RecipeSerializerRead(serializers.ModelSerializer):
    # author = CustomUserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ("id", "ingredients", "name")

    def get_ingredients(self, obj):
        """Получение списка ингредиентов."""
        ingredients = obj.ingredients.values(
            "id",
            "name",
            "measurement_unit",
            "cooked_times",
            amount=F("ingredientinrecipe__amount"))
        return ingredients


class RecipeSerializerWrite(serializers.ModelSerializer):
    ingredients = IngredientInRecipeSerializer(many=True, required=True)

    class Meta:
        model = Recipe
        fields = ("id", "ingredients", "name")  # , 'text', 'cooking_time',)

    def validate_ingredients(self, ingredients):
        """Валидатор ингредиентов"""
        ingredient_list = []
        massage = "Не должно быть повторяющихся ингредиентов"
        for ingredient in ingredients:
            print(ingredient)
            if int(ingredient["amount"]) <= 0:
                raise ValidationError("Выберите кол-во для ингредиента")
            if ingredient["id"] in ingredient_list:
                raise ValidationError([{"ingredient": [massage]}, {}])
            ingredient_list.append(ingredient["id"])
        return ingredients

    def to_representation(self, instance):
        return RecipeSerializerRead(instance, context=self.context).data

    def create_ingredients(self, recipe, ingredients):
        """Создание списка ингредиентов"""
        IngredientInRecipe.objects.bulk_create(
            [
                IngredientInRecipe(
                    recipe=recipe,
                    ingredient=Ingredient.objects.get(pk=ingredient["id"]),
                    amount=ingredient["amount"],
                )
                for ingredient in ingredients
            ]
        )

    def create(self, validated_data):
        # request = self.context.get('request')
        ingredients = validated_data.pop("ingredients")
        recipe = Recipe.objects.create(
            **validated_data)  # author=request.user,
        self.create_ingredients(recipe=recipe, ingredients=ingredients)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop("ingredients")
        instance = super().update(instance, validated_data)
        instance.ingredients.clear()
        self.create_ingredients(recipe=instance, ingredients=ingredients)
        return instance
