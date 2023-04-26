from recipes.models import Tag, Ingredient, Recipe, Shopping_cart, Favorite


def total_cart(user):
    '''Функция формирования списка ингредиентов.
    '''
    recipes = Shopping_cart.objects.filter(user=user.id)
    print('recipes----------->',recipes.recipe)
    ingredients = Recipe.objects.values_list('ingredients',
                                             flat=True
                                             ).filter(id__in=recipes.recipe)


    cart = {}
    for ingredient in ingredients:
        summ = cart.get(ingredient.ingredient, 0)
        summ += ingredient.amount
        cart[ingredient.ingredient] = summ
    shopping_cart = ''
    for i in cart.key.sort():
        shopping_cart += str(cart[i]) + '\n'
    return shopping_cart
