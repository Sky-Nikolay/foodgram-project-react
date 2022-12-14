from collections import Counter

from recipes.models import IngredientRecipe


def get_shopping_cart(user):
    ingredients = IngredientRecipe.objects.filter(
        recipe__shop_list__user=user.user
    )
    compressed_ingredients = Counter()
    for ing in ingredients:
        compressed_ingredients[
            (ing.ingredient.name, ing.ingredient.measurement_unit)
        ] += ing.amount
    return ([
        f"- {name}: {amount} {measurement_unit}\n"
        # скобки ниже в compressed_ingredients необходимы так как там 2 items
        # это сделано для атомарности структуры - Ингедиент-ед.измерения
        for (name, measurement_unit), amount
        in compressed_ingredients.items()
    ])
