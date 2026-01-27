def test_category_equality_and_hash(sample_category):
    from pantry.domainmodel.category import Category

    cat1 = Category("Baking")
    cat2 = sample_category

    assert cat1 == cat2
    assert hash(cat1) == hash(cat2)


def test_ingredient_properties(sample_ingredient):
    ing = sample_ingredient
    assert ing.name == "Sugar"
    assert ing.quantity == 1
    assert ing.unit == "kg"
    # modify
    ing.quantity = 2
    assert ing.quantity == 2


def test_recipe_equality_and_ordering(sample_recipe):
    from pantry.domainmodel.recipe import Recipe

    r1 = sample_recipe
    r2 = Recipe(
        id=1,
        name="Pancakes",
        description="Other",
        ingredients=[],
        methods=[],
        prep_time_mins=0,
        cook_time_mins=0,
        total_time_mins=0,
        difficulty="",
        category="",
        cuisine="",
        tags=[],
        notes="",
        image_url="",
    )

    assert r1 == r2
    assert hash(r1) == hash(r2)


def test_user_grocery_and_recipe_ingredients():
    from pantry.domainmodel.user import User
    from pantry.domainmodel.ingredient import Ingredient

    u = User(1, "u", "u@example.com")
    ing = Ingredient("Tomato", 1, "pc")

    u.add_grocery(ing, 2)
    assert len(u.grocery_list) == 1
    assert u.grocery_list[0].quantity == 2

    u.add_recipe_ingredient("Pancakes", "1 cup flour")
    assert "Pancakes" in u.recipe_ingredients
    u.remove_recipe_ingredient("Pancakes", "1 cup flour")
    assert "Pancakes" not in u.recipe_ingredients

    u.add_multiple_recipe_ingredients("Pancakes", ["1 egg", "1 cup milk"])
    assert len(u.recipe_ingredients["Pancakes"]) == 2
    u.remove_multiple_recipe_ingredients("Pancakes", ["1 egg"])
    assert len(u.recipe_ingredients["Pancakes"]) == 1
    u.clear_recipe_ingredients_by_recipe("Pancakes")
    assert "Pancakes" not in u.recipe_ingredients
