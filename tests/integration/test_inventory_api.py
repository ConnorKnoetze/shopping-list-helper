import json
from tests.utils import make_user, login_user


def test_inventory_api_and_update(client, memory_repo):
    # ensure ingredient exists (from populate)
    ing = memory_repo.get_ingredient_by_name("Carrot")
    assert ing is not None

    # create user and login
    user = make_user(
        memory_repo, username="ivan", email="ivan@example.com", password="Password1"
    )
    login_user(client, "ivan", "Password1")

    # test ingredient api
    resp = client.get(f"/inventory/api/{ing.name}")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["name"] == ing.name

    # update inventory: valid JSON
    payload = {"quantity": 3, "unit": ing.unit}
    resp2 = client.post(f"/inventory/update/{ing.name}", json=payload)
    assert resp2.status_code == 200
    j = resp2.get_json()
    assert j["success"]
    assert str(ing.name) in j["message"]

    # update inventory: invalid JSON
    resp3 = client.post(
        f"/inventory/update/{ing.name}",
        data="notjson",
        headers={"Content-Type": "application/json"},
    )
    assert resp3.status_code in (400, 422)


def test_inventory_api_missing_item(client, memory_repo):
    from tests.utils import make_user, login_user

    user = make_user(
        memory_repo, username="jen", email="jen@example.com", password="Password1"
    )
    login_user(client, "jen", "Password1")

    resp = client.get("/inventory/api/NoSuchIngredient")
    assert resp.status_code == 404

    payload = {"quantity": 2, "unit": "kg"}
    resp2 = client.post("/inventory/update/NoSuchIngredient", json=payload)
    assert resp2.status_code == 404


def test_inventory_api_unauthenticated(client, memory_repo):
    # ensure ingredient exists (from populate)
    ing = memory_repo.get_ingredient_by_name("Carrot")
    assert ing is not None

    # access inventory API without login
    resp = client.get(f"/inventory/api/{ing.name}")
    # login_required redirects to login page when not authenticated
    assert resp.status_code in (301, 302)

    payload = {"quantity": 2, "unit": ing.unit}
    resp2 = client.post(f"/inventory/update/{ing.name}", json=payload)
    assert resp2.status_code in (301, 302)


def test_inventory_api_invalid_unit(client, memory_repo):
    from tests.utils import make_user, login_user

    # ensure ingredient exists (from populate)
    ing = memory_repo.get_ingredient_by_name("Carrot")
    assert ing is not None

    user = make_user(
        memory_repo, username="leo", email="leo@gmail.com", password="Password1"
    )
    login_user(client, "leo", "Password1")
    # update inventory with invalid unit
    payload = {"quantity": 2, "unit": "invalid_unit"}
    resp = client.post(f"/inventory/update/{ing.name}", json=payload)
    assert resp.status_code == 400
    j = resp.get_json()
    assert not j["success"]
    assert "Invalid unit" in j["message"]


def test_inventory_api_negative_quantity(client, memory_repo):
    from tests.utils import make_user, login_user

    # ensure ingredient exists (from populate)
    ing = memory_repo.get_ingredient_by_name("Carrot")
    assert ing is not None

    user = make_user(
        memory_repo, username="mia", email="mia@gmail.com", password="Password1"
    )
    login_user(client, "mia", "Password1")
    # update inventory with negative quantity
    payload = {"quantity": -5, "unit": ing.unit}
    resp = client.post(f"/inventory/update/{ing.name}", json=payload)
    assert resp.status_code == 400
    j = resp.get_json()
    assert not j["success"]
    assert "Quantity cannot be negative" in j["message"]


def test_inventory_api_non_numeric_quantity(client, memory_repo):
    from tests.utils import make_user, login_user

    # ensure ingredient exists (from populate)
    ing = memory_repo.get_ingredient_by_name("Carrot")
    assert ing is not None

    user = make_user(
        memory_repo, username="nina", email="nina@gmail.com", password="Password1"
    )
    login_user(client, "nina", "Password1")
    # update inventory with non-numeric quantity
    payload = {"quantity": "five", "unit": ing.unit}
    resp = client.post(f"/inventory/update/{ing.name}", json=payload)
    assert resp.status_code == 400
    j = resp.get_json()
    assert not j["success"]
    assert "Quantity must be a number" in j["message"]
