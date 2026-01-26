from tests.utils import make_user, login_user


def test_register_and_login_flow(client, memory_repo):
    # register via service to avoid dealing with form CSRF
    user = make_user(memory_repo, username="carol", email="carol@example.com", password="Password1")

    # login
    resp = login_user(client, "carol", "Password1")
    assert resp.status_code == 200
    # logout
    resp2 = client.get("/auth/logout", follow_redirects=True)
    assert resp2.status_code == 200

    # access a protected page
    resp3 = client.get("/shopping", follow_redirects=False)
    assert resp3.status_code in (301, 302)  # should redirect to login
    # follow redirect
    resp4 = client.get("/shopping", follow_redirects=True)
    assert resp4.status_code == 200
    assert b"Login" in resp4.data or b"Please log in to access this page." in resp4.data