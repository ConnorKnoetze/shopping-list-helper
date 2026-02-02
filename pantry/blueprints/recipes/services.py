from pantry.blueprints.services import _repo


def _handle_recipe_ingredients_form(selected, user, recipe_name, repo):
    parsed = []
    display_names = []
    for ingredient in selected:
        parts = ingredient.split(";;")
        if len(parts) < 3:
            parts = (parts + ["", "", ""])[:3]
        parsed.append([parts[0], parts[1], parts[2]])
        display_names.append(parts[2])

    repo.clear_user_recipe_ingredients(user, recipe_name)
    repo.add_multiple_user_recipe_ingredients(user, recipe_name, parsed)

    recipe = repo.get_recipe_by_name(recipe_name)
    recipe_id = recipe.id if recipe is not None and hasattr(recipe, 'id') else recipe
    if not repo.user_has_saved_recipe(recipe_id, user):
        repo.add_saved_recipe(recipe_id, user)

    repo.update_user(user)

    return display_names
