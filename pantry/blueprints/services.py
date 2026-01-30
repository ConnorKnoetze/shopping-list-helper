from pantry.adapters import repository


def _repo():
    r = repository.repo_instance
    if r is None:
        raise RuntimeError("Repository not initialized")
    return r

def get_current_user():
    from flask import session

    repo = _repo()
    username = session.get("username")
    if username:
        return repo.get_user_by_username(username)
    return None