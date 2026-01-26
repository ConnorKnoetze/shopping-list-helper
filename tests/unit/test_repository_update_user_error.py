import pytest


def test_update_user_not_found_raises(memory_repo):
    from pantry.domainmodel.user import User
    from pantry.adapters.memory_repository import MemoryRepository, RepositoryException

    repo = memory_repo
    # create a user object not added to repo
    u = User(9999, "ghost", "ghost@example.com", "hash")

    with pytest.raises(RepositoryException):
        repo.update_user(u)
