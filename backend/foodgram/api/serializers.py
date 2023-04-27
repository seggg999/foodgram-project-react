from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from recipes.models import (Amount, Favorite, Ingredient, IngredientInRecipe,
                            Recipe, Shoppingcart, Tag, TagInRecipe)
from users.models import Subscription

from .field import Base64ImageField

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    '''Пользователь.
    '''
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name',
                  'is_subscribed')

    def get_is_subscribed(self, obj):
        '''Пользователь подписан на автора рецепта.
        '''
        user_id = self.context.get('request').user.id
        return Subscription.objects.filter(author=obj.id,
                                           user=user_id
                                           ).exists()


class CustomUserCreateSerializer(UserCreateSerializer):
    """Создание нового пользователя.
    """
    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name',
                  'password')


class UserWithRecipesSerializer(serializers.ModelSerializer):
    '''Пользователь с рецептами.
    '''
    recipes = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed',
                  'recipes',
                  'recipes_count')
        read_only_fields = ('email', 'username',)

    def validate(self, obj):
        if (self.context['request'].user == obj):
            raise serializers.ValidationError(
                {'errors': 'Нельзя подписаться на себя.'})
        return obj

    def get_is_subscribed(self, obj):
        '''Пользователь подписан на автора рецепта.
        '''
        user_id = self.context.get('request').user.id
        return Subscription.objects.filter(author=obj.id,
                                           user=user_id
                                           ).exists()

    def get_recipes_count(self, obj):
        '''Общее количество рецептов пользователя.
        '''
        return Recipe.objects.filter(id=obj.id).count()

    def get_recipes(self, obj):
        '''Рецепты с огранечением выдачи.
        recipes_limit - Количество объектов внутри поля recipes
        '''
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = Recipe.objects.filter(id=obj.id
                                        )
        if limit:
            recipes = recipes[:int(limit)]
        serializer = RecipeMinifiedSerializer(recipes, many=True,
                                              read_only=True
                                              )
        return serializer.data


class TagSerializer(serializers.ModelSerializer):
    '''Сериализатор Тэгов.
    '''
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    '''Сериализатор Ингредиентов.
    '''
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class AmountSerializer(serializers.ModelSerializer):
    '''Сериализатор колличества ингредиента.
    '''
    class Meta:
        model = Amount
        fields = ('id', 'ingredient', 'amount')


class CreateAmountSerializer(serializers.ModelSerializer):
    '''Сериализатор колличества ингредиента.
    '''
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all())

    class Meta:
        model = Amount
        fields = ('id', 'amount')


class IngredientAmountSerializer(serializers.ModelSerializer):
    '''Сериализатор Ингредиентов c их колличеством.
    '''
    id = serializers.SlugRelatedField(source='ingredient',
                                      slug_field='id',
                                      read_only='True'
                                      )

    name = serializers.SlugRelatedField(source='ingredient',
                                        slug_field='name',
                                        read_only='True'
                                        )

    measurement_unit = serializers.SlugRelatedField(
        source='ingredient', slug_field='measurement_unit', read_only='True')

    class Meta:
        model = Amount
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    '''Сериализатор Рецептов.
    '''
    tags = TagSerializer(read_only=False, many=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientAmountSerializer(read_only=False, many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time')

    def get_is_favorited(self, obj):
        '''Рецепт находится ли в избранном.
        '''
        user_id = self.context['request'].user.id
        return Favorite.objects.filter(recipe=obj.id,
                                       user=user_id,
                                       ).exists()

    def get_is_in_shopping_cart(self, obj):
        '''Рецепт находится ли в корзине.
        '''
        user_id = self.context['request'].user.id
        return Shoppingcart.objects.filter(
            recipe=obj.id, user=user_id).exists()


class CreatRecipeSerializer(RecipeSerializer):
    '''Сериализатор создания Рецептов.
    '''
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all())
    author = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())
    ingredients = CreateAmountSerializer(many=True)

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        for tag in tags:
            TagInRecipe.objects.create(recipe=recipe,
                                       tag=tag
                                       )
        for ingredient in ingredients:
            current_amount = Amount.objects.create(
                amount=ingredient['amount'], ingredient=ingredient['id'])
            IngredientInRecipe.objects.create(recipe=recipe,
                                              ingredient=current_amount
                                              )
        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.image = validated_data.get("image", instance.image)
        instance.text = validated_data.get("text", instance.text)
        instance.cooking_time = validated_data.get("cooking_time",
                                                   instance.cooking_time
                                                   )
        if 'tags' in validated_data:
            tags_data = validated_data.pop('tags')
            lst = []
            for tag in tags_data:
                current_tag = Tag.objects.get(id=tag.id)
                lst.append(current_tag)
            instance.tags.set(lst)
        if 'ingredients' in validated_data:
            ingredients_data = validated_data.pop('ingredients')
            lst = []
            for ingredient in ingredients_data:
                current_ingredient = Amount.objects.create(
                    amount=ingredient.get('amount'),
                    ingredient=ingredient.get('id')
                )
                lst.append(current_ingredient)
            instance.ingredients.set(lst)
        instance.save()
        return instance

    def to_representation(self, instance):
        return RecipeSerializer(instance,
                                context=self.context).data


class RecipeMinifiedSerializer(serializers.ModelSerializer):
    '''Рецепт в сокращенном виде.
    '''
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
