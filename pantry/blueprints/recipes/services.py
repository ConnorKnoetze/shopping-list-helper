from pantry.blueprints.services import _repo

def _handle_recipe_ingredients_form(selected, user, recipe_name,repo):
    selected_ingredients = [ingredient.split(";;")[2] for ingredient in selected]
    handled_ingredients = [ingredient.split(";;") for ingredient in selected]
    repo.clear_user_recipe_ingredients(user, recipe_name)
    repo.add_multiple_user_recipe_ingredients(user, recipe_name, handled_ingredients)

    recipe = repo.get_recipe_by_name(recipe_name)
    if not repo.user_has_saved_recipe(recipe, user):
        repo.add_saved_recipe(recipe, user)

    repo.update_user(user)

    return selected_ingredients