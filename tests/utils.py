from werkzeug.security import generate_password_hash


def make_user(repo, username="test", email="test@example.com", password="Password1"):
    password_hash = generate_password_hash(password)
    user = repo.create_user(username=username, email=email, password_hash=password_hash)
    repo.add_user(user)
    return user


def login_user(client, username, password):
    return client.post(
        "/auth/login",
        data={"username": username, "password": password},
        follow_redirects=True,
    )
