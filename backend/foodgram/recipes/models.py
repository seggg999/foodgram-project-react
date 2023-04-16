# https://docs.djangoproject.com/en/2.2/ref/models/fields/#field-types

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

User = get_user_model()


class Tag(models.Model):
    '''Тэги:
    id     - Уникальный id;
    name   - Название;
    color  - Цвет в HEX;
    slug   - Уникальный слаг.'''

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
        unique=True
    )
    slug = models.SlugField(
        verbose_name='слаг',
        max_length=200,
        unique=True
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    '''Ингредиенты:
    id               - Уникальный id;
    name             - Название ингредиента;
    measurement_unit - Единица измерения ингредиента.'''

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

    def __str__(self):
        return self.name


class Amount(models.Model):
    '''Колличество ингредиента в рецепте:
       amoun      - Колличество ингредиента;
#      recipe     - Рецепт;
       ingredient - Ингредиент;
       amount     - Колличество ингредиента.'''

    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        on_delete=models.CASCADE,
#       related_name='amount_ingredient'
    )
    amount = models.PositiveIntegerField(
        verbose_name='Колличество ингредиента'
    )

    def __str__(self):
        return f'{self.ingredient}'

    class Meta:
        ordering = ['ingredient']


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
    cooking_time   - Время приготовления (в минутах).'''

    id = models.AutoField(primary_key=True)
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Список тегов',
        through='TagInRecipe'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        related_name='author',
        on_delete=models.CASCADE
    )
    ingredients = models.ManyToManyField(
        Amount,
        verbose_name='Список ингредиентов',
        through='IngredientInRecipe'
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=200
    )
    image = models.URLField(
        verbose_name='Картинка',
    )
    text = models.CharField(
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

    def __str__(self):
        return self.name


class Favorite(models.Model):
    '''Избранные рецепты:
    recipe - Рецепт
    user   - Пользователь добавил рецепт в избранное.'''

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
    user   - Пользователь добавил рецепт в корзину.'''

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

    def __str__(self):
        return f'{self.user} {self.recipe}'


class TagInRecipe(models.Model):
    '''Тэги в рецепте:
       recipe - Рецепт;
       tag    - Тэг.'''

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

    def __str__(self):
        return f'{self.recipe} {self.tag}'

    class Meta:
        ordering = ['recipe']


class IngredientInRecipe(models.Model):
    '''Ингредиенты в рецептах:
       recipe     - Рецепт;
       ingredient - Ингредиент.'''

    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Amount,
        verbose_name='Ингредиент',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.recipe} {self.ingredient}'

    class Meta:
        ordering = ['recipe']
