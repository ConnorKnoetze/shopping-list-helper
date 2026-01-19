import abc
from typing import List

repo_instance = None

class RepositoryException(Exception):
    def __init__(self, message=None):
        pass

class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add_ingredient(self, ingredient):
        # Adds an Ingredient to the repository.
        raise NotImplementedError

    @abc.abstractmethod
    def add_multiple_ingredients(self, ingredients: List):
        # Adds multiple Ingredients to the repository.
        raise NotImplementedError

    @abc.abstractmethod
    def get_ingredient_by_name(self, name: str):
        # Retrieves an Ingredient by its name.
        raise NotImplementedError

    @abc.abstractmethod
    def get_ingredients_by_category(self, category: str) -> List:
        # Retrieves Ingredients by their category.
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_ingredients(self) -> List:
        # Retrieves all Ingredients.
        raise NotImplementedError

    @abc.abstractmethod
    def sort_ingredients_by_name(self, name: str):
        raise NotImplementedError
    @abc.abstractmethod
    def sort_ingredients_by_category(self, category: str):
        raise NotImplementedError

    @abc.abstractmethod
    def add_category(self, category):
        # Adds a Category to the repository.
        raise NotImplementedError

    @abc.abstractmethod
    def add_multiple_categories(self, categories: List):
        # Adds multiple Categories to the repository.
        raise NotImplementedError

    @abc.abstractmethod
    def get_category_by_name(self, name: str):
        # Retrieves a Category by its name.
        raise NotImplementedError
    @abc.abstractmethod
    def get_all_categories(self) -> List:
        # Retrieves all Categories.
        raise NotImplementedError
    @abc.abstractmethod
    def add_user(self, user):
        # Adds a User to the repository.
        raise NotImplementedError
    @abc.abstractmethod
    def get_user_by_username(self, username: str):
        # Retrieves a User by their username.
        raise NotImplementedError
    @abc.abstractmethod
    def get_all_users(self) -> List:
        # Retrieves all Users.
        raise NotImplementedError

    @abc.abstractmethod
    def get_total_user_size(self):
        # Retrieves the total number of users.
        raise NotImplementedError

    @abc.abstractmethod
    def create_user(self, username: str, email: str, password_hash: str):
        # Creates a new user.
        raise NotImplementedError

    @abc.abstractmethod
    def get_user_by_email(self, email_clean):
        # Retrieves a User by their email.
        raise NotImplementedError

    @abc.abstractmethod
    def update_user(self, user):
        raise NotImplementedError

