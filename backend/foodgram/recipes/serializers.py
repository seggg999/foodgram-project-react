from rest_framework import serializers
from recipes.models import (Tag, Ingredient, Recipe, Favorite, Shopping_cart,
                            Amount
                            )

from users.serializers import UserSerializer


class TagSerializer(serializers.ModelSerializer):
    '''Сериализатор Тэгов. '''

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    '''Сериализатор Ингредиентов. '''

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class AmountSerializer(serializers.ModelSerializer):
    '''Сериализатор колличества ингредиента. '''

    class Meta:
        model = Amount
        fields = ('id', 'ingredient', 'amount')


class IngredientAmountSerializer(serializers.ModelSerializer):
    '''Сериализатор Ингредиентов c их колличеством. '''

    id = serializers.SlugRelatedField(source='ingredient',
                                      slug_field='id',
                                      read_only='True'
                                      )

    name = serializers.SlugRelatedField(source='ingredient',
                                        slug_field='name',
                                        read_only='True'
                                        )

    measurement_unit = serializers.SlugRelatedField(
        source='ingredient', slug_field='measurement_unit', read_only='True'
        )

    class Meta:
        model = Amount
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    '''Сериализатор Рецептов. '''

    tags = TagSerializer(read_only=True, many=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientAmountSerializer(read_only=True, many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time')

    def get_is_favorited(self, obj):
        '''Рецепт находится ли в избранном. '''
        user_id = self.context['request'].user.id
        return Favorite.objects.filter(recipe=obj.id,
                                       user=user_id,
                                       ).exists()

    def get_is_in_shopping_cart(self, obj):
        '''Рецепт находится ли в корзине. '''
        user_id = self.context['request'].user.id
        return Shopping_cart.objects.filter(recipe=obj.id,
                                            user=user_id,
                                            ).exists()


class RecipeMinifiedSerializer(serializers.ModelSerializer):
    '''Краткий рецепт. '''

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
