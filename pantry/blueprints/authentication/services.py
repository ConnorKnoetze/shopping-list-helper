from werkzeug.security import check_password_hash

from pantry.adapters.repository import AbstractRepository


class NameNotUniqueException(Exception):
    pass


class EmailNotUniqueException(Exception):
    pass


class UnknownUserException(Exception):
    pass


class AuthenticationException(Exception):
    pass


def add_user(username: str, email: str, password_hash: str, repo: AbstractRepository):
    if not username or not isinstance(username, str) or username.strip() == "":
        raise ValueError("username is required")

    print(username, email, password_hash)

    username_clean = username.strip()
    email_clean = email.strip()

    existing_username = repo.get_user_by_username(username_clean)
    existing_email = repo.get_user_by_email(email_clean)

    if existing_username is not None:
        raise NameNotUniqueException
    if existing_email is not None:
        raise EmailNotUniqueException

    new_user = repo.create_user(
        username=username_clean, email=email_clean, password_hash=password_hash
    )
    repo.add_user(new_user)

    print(new_user)

    return new_user


def get_user(username: str, repo: AbstractRepository):
    user = repo.get_user_by_username(username)

    if user is None:
        print(
            f"DEBUG: get_user - no user for '{username}' (repo: {repo.__class__.__name__})"
        )
        raise UnknownUserException
    return user_to_dict(user)


def authenticate_user(username: str, password_hash: str, repo: AbstractRepository):
    authenticated = False
    user = repo.get_user_by_username(username)

    authenticated = check_password_hash(user.password_hash, password_hash)
    if not authenticated:
        raise AuthenticationException


def user_to_dict(user) -> dict:
    user_dict = {
        "user_id": str(user.id),
        "email": user.email,
        "username": user.username,
        "password": user.password_hash,
    }
    return user_dict
