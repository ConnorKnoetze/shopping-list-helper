from flask import session

from pantry.adapters import repository


def get_current_user():
    username = session.get("username")
    if not username:
        return None
    repo = repository.repo_instance
    if repo is None:
        return None
    user = repo.get_user_by_username(username)
    return user


def is_logged_in():
    username = session.get("username")

    if not username:
        return False

    repo = repository.repo_instance

    if repo is None:
        return False

    user = repo.get_user_by_username(username)

    return user is not None