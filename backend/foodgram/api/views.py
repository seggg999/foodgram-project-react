from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from users.models import Subscription

from foodgram.settings import FILE_NAME
from recipes.models import (Amount, Favorite, Ingredient, IngredientInRecipe,
                            Recipe, Shoppingcart, Tag)

from .filters import RecipeFilter
from .pagination import CustomPaginator
from .permissions import IsAutherOrReadOnly
from .serializers import (CreatRecipeSerializer, IngredientSerializer,
                          RecipeMinifiedSerializer, RecipeSerializer,
                          TagSerializer, UserWithRecipesSerializer)

User = get_user_model()


class CastomDjUserViewSet(UserViewSet):
    '''Кастомный djoser UserViewSet.
    '''

    @action(["get"], detail=False, permission_classes=[IsAuthenticated])
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        return self.retrieve(request, *args, **kwargs)

    @action(["get"], detail=False,
            permission_classes=[IsAuthenticated],
            pagination_class=CustomPaginator)
    def subscriptions(self, request, *args, **kwargs):
        '''Мои подписки.
        '''
        follow = Subscription.objects.values_list(
            'author', flat=True).filter(user=request.user)
        follow_list = User.objects.filter(id__in=follow)
        page = self.paginate_queryset(follow_list)
        serializer = UserWithRecipesSerializer(page, many=True,
                                               context={'request': request}
                                               )
        return self.get_paginated_response(serializer.data)

    @action(["post", "delete"], detail=True,
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, id=None):
        '''Добавить/убрать рецепт в/из подписки.
        '''
        author_obj = get_object_or_404(User, id=id)
        user_obj = request.user
        sub_post = Subscription.objects.filter(author=author_obj.id,
                                               user=user_obj.id,
                                               )
        if request.method == 'POST':
            if sub_post.exists():
                mess = {"errors": "Пользователь уже подписан на автора!"}
                return Response(mess, status=status.HTTP_400_BAD_REQUEST)
            Subscription.objects.create(author=author_obj,
                                        user=user_obj,
                                        )
            serializer = UserWithRecipesSerializer(author_obj,
                                                   context={'request': request}
                                                   )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if sub_post.exists():
            sub_post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        mess = {"errors": "Пользователь не был подписан на автора!"}
        return Response(mess, status=status.HTTP_400_BAD_REQUEST)

    def activation(self, request, *args, **kwargs):
        '''pass'''
        return Response(status=status.HTTP_404_NOT_FOUND)

    def resend_activation(self, request, *args, **kwargs):
        '''pass'''
        return Response(status=status.HTTP_404_NOT_FOUND)

    def reset_password(self, request, *args, **kwargs):
        '''pass'''
        return Response(status=status.HTTP_404_NOT_FOUND)

    def reset_password_confirm(self, request, *args, **kwargs):
        '''pass'''
        return Response(status=status.HTTP_404_NOT_FOUND)

    def set_username(self, request, *args, **kwargs):
        '''pass'''
        return Response(status=status.HTTP_404_NOT_FOUND)

    def reset_username(self, request, *args, **kwargs):
        '''pass'''
        return Response(status=status.HTTP_404_NOT_FOUND)

    def reset_username_confirm(self, request, *args, **kwargs):
        '''pass'''
        return Response(status=status.HTTP_404_NOT_FOUND)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    pagination_class = None
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAutherOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    http_method_names = ['get', 'options', 'post', 'head', 'delete', 'patch']

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreatRecipeSerializer
        if self.request.method == "PATCH":
            return CreatRecipeSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        super().perform_create(serializer)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)
        super().perform_update(serializer)

    @action(["get"], detail=False,
            permission_classes=[IsAuthenticated]
            )
    def download_shopping_cart(self, request, *args, **kwargs):
        '''Скачать файл со списком покупок.'''
        ingredients_list = (
            IngredientInRecipe.objects
            .filter(recipe__shop_recipe__user=request.user)
            .values_list('ingredient', flat=True)
        )
        ingredients = (
            Amount.objects.filter(id__in=ingredients_list)
            .values('ingredient')
            .annotate(total_amount=Sum('amount'))
            .values_list('ingredient__name', 'total_amount',
                         'ingredient__measurement_unit')
        )
        file_list = ['Список покупок:\n']
        [file_list.append(
            '{} - {} {}.\n'.format(*ingredient)) for ingredient in ingredients]
        response = HttpResponse(file_list, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={FILE_NAME}'
        return response

    @action(["post", "delete"], detail=True,
            permission_classes=[IsAuthenticated]
            )
    def shopping_cart(self, request, pk=None):
        '''Добавить/удалить рецепт в список покупок.'''
        recipe_obj = get_object_or_404(Recipe, id=pk)
        user_obj = self.request.user
        sub_post = Shoppingcart.objects.filter(
            recipe=recipe_obj, user=user_obj)
        if request.method == 'POST':
            if sub_post.exists():
                mess = {"errors": "Рецепт уже был добавлен в список покупок!"}
                return Response(mess, status=status.HTTP_400_BAD_REQUEST)
            Shoppingcart.objects.create(
                recipe=recipe_obj, user=user_obj)
            serializer = RecipeMinifiedSerializer(recipe_obj)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if sub_post.exists():
            sub_post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        mess = {"errors": "Рецепт еще не был добавлен в список покупок!"}
        return Response(mess, status=status.HTTP_400_BAD_REQUEST)

    @action(["post", "delete"], detail=True,
            permission_classes=[IsAuthenticated]
            )
    def favorite(self, request, pk=None):
        '''Добавить/удалить рецепт в избранное.'''
        recipe_obj = get_object_or_404(Recipe, id=pk)
        user_obj = self.request.user
        sub_post = Favorite.objects.filter(recipe=recipe_obj,
                                           user=user_obj,
                                           )
        if request.method == 'POST':
            if sub_post.exists():
                mess = {"errors": "Рецепт уже был добавлен в избранное!"}
                return Response(mess, status=status.HTTP_400_BAD_REQUEST)
            Favorite.objects.create(recipe=recipe_obj,
                                    user=user_obj,
                                    )
            serializer = RecipeMinifiedSerializer(recipe_obj)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if sub_post.exists():
            sub_post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        mess = {"errors": "Рецепт еще не был добавлен в избранное!"}
        return Response(mess, status=status.HTTP_400_BAD_REQUEST)
