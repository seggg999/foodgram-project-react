from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (TagViewSet, RecipeViewSet, IngredientViewSet)

app_name = 'recipes'


router = DefaultRouter()

router.register('tags', TagViewSet)
router.register('recipes', RecipeViewSet)
router.register('ingredients', IngredientViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
