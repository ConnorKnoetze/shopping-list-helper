from tests.utils import make_user, login_user


def test_toggle_save_recipe_and_post_ingredients(client, memory_repo):
    # create a user and add a recipe
    user = make_user(memory_repo, username="sam", email="sam@example.com", password="Password1")
    from pantry.domainmodel.recipe import Recipe
    from pantry.domainmodel.ingredient import Ingredient

    ing = Ingredient("Sugar", 1, "kg")
    r = Recipe(
        id=50,
        name="Jam",
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

    login_user(client, "sam", "Password1")

    # initially not saved
    resp = client.post(f"/recipes/toggle_save/{r.name.replace(' ', '-')}")
    assert resp.status_code == 200
    j = resp.get_json()
    assert j["saved"] is True

    # toggle again
    resp2 = client.post(f"/recipes/toggle_save/{r.name.replace(' ', '-')}")
    assert resp2.status_code == 200
    j2 = resp2.get_json()
    assert j2["saved"] is False

    # POST to recipe detail to set ingredients
    payload = {"ingredients[]": ["1;;cup;;flour"]}
    resp3 = client.post(f"/recipes/{r.name.replace(' ', '-')}", data=payload)
    assert resp3.status_code == 200
