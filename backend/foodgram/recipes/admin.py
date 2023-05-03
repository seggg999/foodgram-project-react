from django.contrib import admin

from .models import (AmountOfIngredient, Favorite, Ingredient,
                     IngredientInRecipe, Recipe, Shoppingcart, Tag,
                     TagInRecipe)


class IngredientInRecipeInline(admin.StackedInline):
    model = IngredientInRecipe
    list_display = (
        'recipe',
    )


class TagInRecipeInline(admin.StackedInline):
    model = TagInRecipe
    list_display = (
        'tag',
    )


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'author',
        'name',
        'in_favorites'
    )
    readonly_fields = ('in_favorites',)
    inlines = [IngredientInRecipeInline, TagInRecipeInline]
    list_filter = ('author', 'name', 'tags',)
    empty_value_display = '-пусто-'

    @admin.display(description='В избранном')
    def in_favorites(self, obj):
        return obj.favorit_recipe.count()


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'color',
        'slug',
    )
    empty_value_display = '-пусто-'


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'measurement_unit',
    )
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


class ShoppingcartAdmin(admin.ModelAdmin):
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
    empty_value_display = '-пусто-'


class IngredientInRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'recipe',
        'ingredient',
    )
    empty_value_display = '-пусто-'


class AmountOfIngredientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'ingredient',
        'amount',
    )
    search_fields = ('ingredient',)
    list_filter = ('ingredient',)
    empty_value_display = '-пусто-'


admin.site.register(Tag, TagAdmin)
admin.site.register(TagInRecipe, TagInRecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientInRecipe, IngredientInRecipeAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Shoppingcart, ShoppingcartAdmin)
admin.site.register(AmountOfIngredient, AmountOfIngredientAdmin)
