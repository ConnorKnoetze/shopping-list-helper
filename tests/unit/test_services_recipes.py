from pantry.blueprints.recipes.services import _handle_recipe_ingredients_form


def test_handle_recipe_ingredients_form(memory_repo, sample_recipe):
    user = memory_repo.get_user_by_username("CNK")
    # ensure recipe exists
    memory_repo.add_recipe(sample_recipe)

    selected = ["1;;cup;;flour"]
    selected_values = _handle_recipe_ingredients_form(
        selected, user, sample_recipe.name, memory_repo
    )

    assert selected_values == ["flour"]
    # should mark recipe as saved
    assert memory_repo.user_has_saved_recipe(sample_recipe, user)
    # stored ingredients should be present
    assert memory_repo.get_user_recipe_ingredients_by_recipe_name(
        user, sample_recipe.name
    ) == [["1", "cup", "flour"]]
