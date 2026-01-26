import pytest
from pantry import create_app
from pantry.adapters.memory_repository import MemoryRepository
from pantry.adapters import repository


@pytest.fixture
def app():
    # ensure tests run with memory repository and testing config
    import os

    os.environ["REPOSITORY"] = "memory"
    os.environ["TESTING"] = "true"
    app = create_app()
    # test config adjustments
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["SECRET_KEY"] = "test-secret"
    app.testing = True

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def memory_repo(app):
    # return the repo instance initialized by create_app
    return repository.repo_instance


@pytest.fixture
def sample_ingredient():
    from pantry.domainmodel.ingredient import Ingredient

    return Ingredient(name="Sugar", quantity=1, unit="kg")


@pytest.fixture
def sample_category():
    from pantry.domainmodel.category import Category

    return Category(name="Baking")


@pytest.fixture
def sample_recipe(sample_ingredient):
    from pantry.domainmodel.recipe import Recipe

    return Recipe(
        id=1,
        name="Pancakes",
        description="Tasty",
        ingredients=[sample_ingredient],
        methods=["mix", "cook"],
        prep_time_mins=10,
        cook_time_mins=5,
        total_time_mins=15,
        difficulty="Easy",
        category="Breakfast",
        cuisine="American",
        tags=["sweet"],
        notes="",
        image_url="",
    )
