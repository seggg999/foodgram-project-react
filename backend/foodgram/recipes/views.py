from rest_framework import viewsets  # , mixins, filters, status
from rest_framework.permissions import (IsAuthenticated, AllowAny,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.decorators import action

from recipes.models import Tag, Ingredient, Recipe
from .serializers import (
    TagSerializer, IngredientSerializer, RecipeSerializer
)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None
#    filter_backends = (filters.SearchFilter,)
#    search_fields = ('name',)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    pagination_class = None
#    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
#    pagination_class = LimitOffsetPagination
#    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    http_method_names = ['get', 'options', 'post', 'head', 'delete', 'patch']

#    def get_serializer_class(self):
#        if self.action == "create":
#            return settings.SERIALIZERS.user_create
#        elif self.action == "destroy":
#            return settings.SERIALIZERS.user_delete

    @action(["get"], detail=False,
            permission_classes=[IsAuthenticated]
            )
    def download_shopping_cart(self, request, *args, **kwargs):
        '''Скачать список покупок.'''
        self.get_object = self.get_instance
        return self.retrieve(request, *args, **kwargs)

    @action(["post", "delete"], detail=True)
    def shopping_cart(self, request, pk=None):
        '''Добавить/удалить рецепт в список покупок. '''
        self.get_object = self.get_instance
        return self.retrieve(request)

    @action(["post", "delete"], detail=True)
    def favorite(self, request, pk=None):
        '''Добавить/удалить рецепт в избранное. '''
        self.get_object = self.get_instance
        return self.retrieve(request)
