from rest_framework import serializers

from django.contrib.auth import get_user_model
from djoser.conf import settings
from djoser.serializers import UserSerializer, UserCreateSerializer

from recipes.serializers import RecipeMinifiedSerializer
from recipes.models import Recipe
from users.models import Subscription

User = get_user_model()


class UserSerializer(UserSerializer):
    '''Пользователь. '''

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.LOGIN_FIELD,
            settings.USER_ID_FIELD,
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
        )
        read_only_fields = (settings.LOGIN_FIELD,)

    def get_is_subscribed(self, obj):
        '''Пользователь подписан на автора рецепта'''

        user_id = self.context.get('request').user.id
        return Subscription.objects.filter(author=obj.id,
                                           user=user_id
                                           ).exists()


class UserCreateSerializer(UserCreateSerializer):
    '''Создать пользователя. '''

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.LOGIN_FIELD,
            settings.USER_ID_FIELD,
            "first_name",
            "last_name",
            "password",
        )


class UserWithRecipesSerializer(serializers.ModelSerializer):
    '''Пользователь с рецептами.'''

    recipes = RecipeMinifiedSerializer(read_only=True, many=True)
    is_subscribed = serializers.SerializerMethodField()
    recipes = RecipeMinifiedSerializer()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        '''Пользователь подписан на автора рецепта'''

        user_id = self.context.get('request').user.id
        return Subscription.objects.filter(author=obj.id,
                                           user=user_id
                                           ).exists()

    def get_recipes_count(self, obj):
        '''Общее количество рецептов пользователя'''

        recipes_count = Recipe.objects.get(count=obj.id
                                           ).count()
        return recipes_count
