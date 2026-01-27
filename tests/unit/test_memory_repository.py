def test_memory_repository_basic_ops(
    memory_repo, sample_ingredient, sample_category, sample_recipe
):
    # add and retrieve ingredient
    memory_repo.add_ingredient(sample_ingredient)
    ing = memory_repo.get_ingredient_by_name("Sugar")
    assert ing is not None
    assert ing.name == "Sugar"
    assert ing.unit == sample_ingredient.unit

    # categories
    memory_repo.add_category(sample_category)
    assert memory_repo.get_category_by_name("Baking") == sample_category

    # users
    initial_users = memory_repo.get_total_user_size()
    new_user = memory_repo.create_user("john", "john@example.com", "hash")
    memory_repo.add_user(new_user)
    assert memory_repo.get_total_user_size() == initial_users + 1
    assert memory_repo.get_user_by_username("john").username == "john"

    # recipes
    memory_repo.add_recipe(sample_recipe)
    assert memory_repo.get_recipe_by_name("Pancakes").name == "Pancakes"


def test_user_saved_recipe_and_ingredients(memory_repo, sample_recipe):
    user = memory_repo.get_user_by_username("CNK")
    memory_repo.add_saved_recipe(sample_recipe, user)
    assert memory_repo.user_has_saved_recipe(sample_recipe, user)
    memory_repo.remove_saved_recipe(sample_recipe, user)
    assert not memory_repo.user_has_saved_recipe(sample_recipe, user)

    # recipe ingredients manipulation
    memory_repo.add_user_recipe_ingredient(user, sample_recipe.name, "1 cup flour")
    assert "1 cup flour" in memory_repo.get_user_recipe_ingredients_by_recipe_name(
        user, sample_recipe.name
    )
    memory_repo.clear_user_recipe_ingredients(user, sample_recipe.name)
    assert (
        memory_repo.get_user_recipe_ingredients_by_recipe_name(user, sample_recipe.name)
        == []
    )
