def test_recipes_list_and_detail(client, memory_repo):
    from tests.utils import make_user, login_user

    # create user and recipe
    user = make_user(
        memory_repo, username="bob", email="bob@example.com", password="Password1"
    )
    # add a recipe object
    from pantry.domainmodel.recipe import Recipe
    from pantry.domainmodel.ingredient import Ingredient

    ing = Ingredient("Flour", 1, "cup")

    r = Recipe(
        id=2,
        name="Test Recipe",
        description="x",
        ingredients=[ing],
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
    memory_repo.add_recipe(r)

    login_user(client, "bob", "Password1")

    resp = client.get("/recipes", follow_redirects=True)
    assert resp.status_code == 200

    # detail page
    resp2 = client.get(f"/recipes/{r.name.replace(' ', '-')}", follow_redirects=True)
    assert resp2.status_code == 200
    assert b"Test Recipe" in resp2.data or b"Test-Recipe" in resp2.data
