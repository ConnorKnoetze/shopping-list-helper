from tests.utils import make_user, login_user


def test_shopping_remove_and_download(client, memory_repo):
    # create user and add grocery
    user = make_user(
        memory_repo, username="kate", email="kate@example.com", password="Password1"
    )
    # ensure an ingredient exists
    ing = memory_repo.get_ingredient_by_name("Carrot")
    assert ing is not None

    # add grocery to user and update
    user.add_grocery(ing, 2)
    memory_repo.update_user(user)

    login_user(client, "kate", "Password1")

    # remove existing
    resp = client.post(f"/shopping/api/remove/{ing.name}")
    assert resp.status_code == 200
    j = resp.get_json()
    assert j["success"]

    # remove missing
    resp2 = client.post(f"/shopping/api/remove/{ing.name}")
    assert resp2.status_code == 404

    # download shopping list
    user.add_grocery(ing, 1)
    memory_repo.update_user(user)
    resp3 = client.get("/shopping/api/download")
    assert resp3.status_code == 200
    j2 = resp3.get_json()
    assert "Grocery List" in j2["shopping_list"]
