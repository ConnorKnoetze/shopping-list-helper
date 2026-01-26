def test_home_requires_login(client):
    # unauthenticated should redirect to login
    resp = client.get("/", follow_redirects=False)
    assert resp.status_code in (301, 302)


def test_home_page_logged_in(client, memory_repo):
    from tests.utils import make_user, login_user

    user = make_user(memory_repo, username="alice", email="alice@example.com", password="Password1")
    # login
    resp = login_user(client, "alice", "Password1")
    assert resp.status_code == 200
    # access home
    resp2 = client.get("/", follow_redirects=True)
    assert resp2.status_code == 200
    assert b"ingredients" in resp2.data or b"Home" in resp2.data

def test_home_page_content(client, memory_repo):
    from tests.utils import make_user, login_user

    user = make_user(memory_repo, username="dave", email="dave@dave.com", password="Password1")
    # login
    resp = login_user(client, "dave", "Password1")
    assert resp.status_code == 200
    # access home
    resp2 = client.get("/", follow_redirects=True)
    assert resp2.status_code == 200
    # Check for specific content from templates/home.html
    assert b"PantryPal" in resp2.data
    assert b"Your personal pantry management solution" in resp2.data
    assert b"View Recipes" in resp2.data
    assert b"Start Shopping" in resp2.data or b"Start Shopping List" in resp2.data

def test_home_page_no_ingredients_message(client, memory_repo):
    from tests.utils import make_user, login_user

    user = make_user(memory_repo, username="eve", email="eve@gmail.com", password="Password1")
    # login
    resp = login_user(client, "eve", "Password1")
    assert resp.status_code == 200

    # Temporarily clear repository ingredients so the template shows the "no items" path
    repo = memory_repo
    # access the mangled private attribute used in MemoryRepository
    attr_name = "_MemoryRepository__ingredients"
    original_ings = getattr(repo, attr_name)
    try:
        setattr(repo, attr_name, [])
        # access home
        resp2 = client.get("/", follow_redirects=True)
        assert resp2.status_code == 200
        # Check for no ingredients message from the template
        assert b"No ingredients available." in resp2.data
        # Button text exists
        assert b"Start Shopping List" in resp2.data or b"Start Shopping" in resp2.data
    finally:
        # restore original ingredients
        setattr(repo, attr_name, original_ings)

def test_home_page_ingredient_listed(client, memory_repo):
    from tests.utils import make_user, login_user

    user = make_user(memory_repo, username="frank", email="frank@gmail.com", password="Password1")
    # login
    resp = login_user(client, "frank", "Password1")
    assert resp.status_code == 200
    # access home
    resp2 = client.get("/", follow_redirects=True)
    assert resp2.status_code == 200

    # Get the first page of ingredients from the repo and ensure at least one name appears
    ingredient_list = memory_repo.get_all_ingredients()[:10]
    # Build a list of candidate names (string) to search for
    candidate_names = [getattr(i, 'name', str(i)) for i in ingredient_list]

    assert any(name.encode() in resp2.data for name in candidate_names), "No ingredient names from repo found in home page output"

    # Check that the ingredients grid / card markup is present
    assert b"ingredients-grid" in resp2.data or b"inventory-card" in resp2.data or b"item-name" in resp2.data
