from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Название ингредиента",
    )
    measurement_unit = models.TextField(max_length=200,
                                        verbose_name="единицы измерения")
    cooked_times = models.PositiveIntegerField(
        default=0,
        verbose_name="Количество раз приготовлен",
        validators=[MinValueValidator(0)],
    )

    class Meta:
        verbose_name_plural = "Ингредиенты"
        verbose_name = "Ингредиент"

    def __str__(self):
        return f"{self.name} {self.cooked_times} {self.measurement_unit} "


class Recipe(models.Model):
    name = models.TextField(verbose_name="Название", max_length=200,
                            help_text="Введите название")
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name="recipes",
        verbose_name="ингредиенты",
        help_text="Ингредиент из таблицы Ingredient",
        through="IngredientInRecipe",
    )
    # text = models.TextField(
    #     verbose_name='Описание',
    #     help_text='Введите описание')
    # author = models.ForeignKey(
    #     User,
    #     on_delete=models.CASCADE,
    #     related_name='recipes',
    #     verbose_name='Автор рецепта',
    #     help_text='Автор из таблицы User')
    # cooking_time = models.PositiveIntegerField(
    #     verbose_name='Время приготовления (в минутах)',
    #     validators=[MinValueValidator(1)],)

    class Meta:
        verbose_name_plural = "Рецепты"
        verbose_name = "Рецепты"
        ordering = ("-id",)

    def __str__(self):
        return self.name[:15]


class IngredientInRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name="ингредиенты",
        on_delete=models.CASCADE)
    recipe = models.ForeignKey(
        Recipe,
        verbose_name="рецепты",
        related_name="ingredient_list",
        on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Количество",
        help_text="Количество ингредиентов",
    )

    class Meta:
        verbose_name = "Ингредиент-рецепт"
        verbose_name_plural = "Ингредиент-рецепт"
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "ingredient"],
                name="Не должно быть одинаковых ингредиентов!")]

    def __str__(self):
        return f"""{self.ingredient.name}{self.ingredient.measurement_unit} -
          {self.amount} """
