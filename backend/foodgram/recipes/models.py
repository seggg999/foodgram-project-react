# https://docs.djangoproject.com/en/2.2/ref/models/fields/#field-types

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
from django.db.models.signals import post_delete
from django.dispatch import receiver


User = get_user_model()


class Tag(models.Model):
    '''Тэги:
    id     - Уникальный id;
    name   - Название;
    color  - Цвет в HEX;
    slug   - Уникальный слаг.
    '''
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        verbose_name='Тэг',
        max_length=200,
        unique=True,
        db_index=True
    )
    color = models.CharField(
        verbose_name='Цвет',
        max_length=7,
        unique=True,
        validators=[
            RegexValidator(regex='^#[0-9A-H]{6}',
                           message='color должен быть в формате ^#[0-9A-H]{6}',
                           code='invalid_color_regex'
                           ),
        ]
    )
    slug = models.SlugField(
        verbose_name='слаг',
        max_length=200,
        unique=True
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    '''Ингредиенты:
    id               - Уникальный id;
    name             - Название ингредиента;
    measurement_unit - Единица измерения ингредиента.
    '''
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        verbose_name='Ингредиент',
        max_length=200,
        db_index=True
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=200
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Amount(models.Model):
    '''Содержание ингредиента в рецепте:
    amoun      - Колличество ингредиента;
#   recipe     - Рецепт;
    ingredient - Ингредиент;
    amount     - Колличество ингредиента.
    '''
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        on_delete=models.CASCADE,
    )
    amount = models.PositiveIntegerField(
        verbose_name='Колличество ингредиента'
    )

    class Meta:
        ordering = ['ingredient']
        verbose_name = 'Содержание ингредиента в рецепте'
        verbose_name_plural = 'Содержание ингредиентов в рецепте'

    def __str__(self):
        return f'{self.ingredient}'


class Recipe(models.Model):
    '''Рецепты:
    id             - Уникальный id;
    tags           - Список тегов;
    author         - Автор рецепта;
    ingredients    - Список ингредиентов;
    is_favorited   - Находится ли в избранном;
    is_in_shopping_cart - Находится ли в корзине;
    name           - Название;
    image          - Ссылка на картинку на сайте;
    text           - Описание;
    cooking_time   - Время приготовления (в минутах).
    '''
    id = models.AutoField(primary_key=True)
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Список тегов',
        through='TagInRecipe',
        db_index=True
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        related_name='author',
        on_delete=models.CASCADE,
        db_index=True
    )
    ingredients = models.ManyToManyField(
        Amount,
        verbose_name='Список ингредиентов',
        through='IngredientInRecipe'
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
        db_index=True
    )
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='recipes/images/',
        )
    text = models.TextField(
        verbose_name='Описание',
        max_length=200
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления',
        validators=[
            MinValueValidator(1),
        ]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class Favorite(models.Model):
    '''Избранные рецепты:
    user   - Пользователь добавил рецепт в избранное;
    recipe - Рецепт.
    '''
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='favorit_user'
    )

    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='favorit_recipe'
    )

    class Meta:
        ordering = ['user']
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            models.UniqueConstraint(
                name="unique_favorite",
                fields=['recipe', 'user'],
            ),
        ]

    def __str__(self):
        return f'{self.user} {self.recipe}'


class Shopping_cart(models.Model):
    '''Список покупок:
    recipe - Рецепт
    user   - Пользователь добавил рецепт в корзину.
    '''
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='shop_recipe'
    )
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='shop_user'
    )

    class Meta:
        ordering = ['user']
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        constraints = [
            models.UniqueConstraint(
                name="unique_shopping_cart",
                fields=['recipe', 'user'],
            ),
        ]

    def __str__(self):
        return f'{self.user} {self.recipe}'


class TagInRecipe(models.Model):
    '''Тэги в рецепте:
    recipe - Рецепт;
    tag    - Тэг.
    '''
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE
    )
    tag = models.ForeignKey(
        Tag,
        verbose_name='Тэг',
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ['recipe']
        verbose_name = 'Тэг в рецепте'
        verbose_name_plural = 'Тэги в рецепте'
        constraints = [
            models.UniqueConstraint(
                name="unique_tag_in_recipe",
                fields=['recipe', 'tag'],
            ),
        ]

    def __str__(self):
        return f'{self.recipe} {self.tag}'


class IngredientInRecipe(models.Model):
    '''Ингредиенты в рецептах:
    recipe     - Рецепт;
    ingredient - Ингредиент.
    '''
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='recipe_in'
    )
    ingredient = models.OneToOneField(
        Amount,
        verbose_name='Ингредиент',
        on_delete=models.CASCADE,
        related_name='ingredient_in'
    )

    class Meta:
        ordering = ['recipe']
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'
        constraints = [
            models.UniqueConstraint(
                name="unique_ingredient_in_recipe",
                fields=['recipe', 'ingredient'],
            ),
        ]

    def __str__(self):
        return f'{self.recipe} {self.ingredient}'


@receiver(post_delete, sender=IngredientInRecipe)
def auto_delete_amount_with_ingredientinrecipe(sender, instance, **kwargs):
    instance.ingredient.delete()
