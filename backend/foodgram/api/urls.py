from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (CastomDjUserViewSet, TagViewSet, RecipeViewSet,
                    IngredientViewSet)

app_name = 'api'


router = DefaultRouter()

router.register('users', CastomDjUserViewSet)
router.register('tags', TagViewSet)
router.register('recipes', RecipeViewSet)
router.register('ingredients', IngredientViewSet)


urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]
