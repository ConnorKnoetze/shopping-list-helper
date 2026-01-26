import pytest
from pantry.blueprints.authentication import services


def test_add_user_valid_and_invalid(memory_repo):
    # valid creation
    password_hash = "hash"
    new_user = memory_repo.create_user("u1", "u1@example.com", password_hash)
    memory_repo.add_user(new_user)
    assert memory_repo.get_user_by_username("u1").email == "u1@example.com"

    # invalid username
    with pytest.raises(ValueError):
        services.add_user("   ", "x@x.com", password_hash, memory_repo)

    # duplicate username
    with pytest.raises(services.NameNotUniqueException):
        services.add_user("u1", "other@example.com", password_hash, memory_repo)

    # duplicate email
    with pytest.raises(services.EmailNotUniqueException):
        services.add_user("another", "u1@example.com", password_hash, memory_repo)


def test_authenticate_user_failure(memory_repo):
    from werkzeug.security import generate_password_hash

    pw = "Secret1"
    user = memory_repo.create_user("authuser", "auth@example.com", generate_password_hash(pw))
    memory_repo.add_user(user)

    with pytest.raises(services.AuthenticationException):
        services.authenticate_user("authuser", "wrongpassword", memory_repo)

    # unknown user in get_user
    with pytest.raises(services.UnknownUserException):
        services.get_user("nonexistent", memory_repo)
