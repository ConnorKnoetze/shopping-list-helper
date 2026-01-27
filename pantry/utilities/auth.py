from flask import session

from pantry.blueprints.services import _repo


def get_current_user():
    username = session.get("username")
    if not username:
        return None
    repo = _repo()
    if repo is None:
        return None
    user = repo.get_user_by_username(username)
    return user


def is_logged_in():
    username = session.get("username")

    if not username:
        return False

    repo = _repo()

    if repo is None:
        return False

    user = repo.get_user_by_username(username)

    return user is not None
