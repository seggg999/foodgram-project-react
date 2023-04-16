from django.contrib import admin

from .models import (Tag, Ingredient, Recipe, Favorite, Amount,
                     Shopping_cart, TagInRecipe, IngredientInRecipe)


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'author',
        'name',
        'image',
        'text',
        'cooking_time',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'color',
        'slug',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'measurement_unit',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'recipe',
    )
    search_fields = ('user',)
    list_filter = ('user',)
    empty_value_display = '-пусто-'


class Shopping_cartAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'recipe',
        'user',
    )
    search_fields = ('user',)
    list_filter = ('user',)
    empty_value_display = '-пусто-'


class TagInRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'recipe',
        'tag',
    )
    search_fields = ('recipe',)
    list_filter = ('recipe',)
    empty_value_display = '-пусто-'


class IngredientInRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'recipe',
        'ingredient',
    )
    search_fields = ('recipe',)
    list_filter = ('recipe',)
    empty_value_display = '-пусто-'


class AmountAdmin(admin.ModelAdmin):
    list_display = (
        'id',
 #       'recipe',
        'ingredient',
        'amount',
    )
    search_fields = ('ingredient',)
    list_filter = ('ingredient',)
    empty_value_display = '-пусто-'


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Shopping_cart, Shopping_cartAdmin)
admin.site.register(TagInRecipe, TagInRecipeAdmin)
admin.site.register(IngredientInRecipe, IngredientInRecipeAdmin)
admin.site.register(Amount, AmountAdmin)
