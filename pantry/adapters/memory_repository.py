from pantry.adapters.repository import AbstractRepository, RepositoryException
from typing import List

from pantry.domainmodel import recipe
from pantry.domainmodel.ingredient import Ingredient
from pantry.domainmodel.category import Category
from pantry.domainmodel.user import User
from pantry.domainmodel.recipe import Recipe


class MemoryRepository(AbstractRepository):
    def __init__(self):
        self.__ingredients: List[Ingredient] = []
        self.__categories: List[Category] = []
        self.__users: List[User] = [
            User(
                user_id=1,
                username="CNK",
                email="connorknoetze@gmail.com",
                password_hash="scrypt:32768:8:1$8B3wBNdfVYip2e7v$7e6807f0c31ca8718ee1b4ed9d0e22ce715a52c15bc5eb273c9e7d6d87169aa9436c0802fccd061192557281aa258a18e1dac4bd44814e6ba8e7852aeccae19d",
            ),
            User(
                user_id=2,
                username="Connor",
                email="example@gmail.com",
                password_hash="scrypt:32768:8:1$6JSrcBOnzaJfWwN6$652022ef1b69f25d9022d975e087090c8271623515cdda680920bb415d6ee4dd5b2a6315d86424e64da2a69c35a2d02fe9d0a3dfb58538107c416dffe4626678"

            )
        ]
        self.__recipes: List[recipe] = []

    def add_ingredient(self, ingredient: Ingredient):
        self.__ingredients.append(ingredient)

    def add_multiple_ingredients(self, ingredients: List[Ingredient]):
        self.__ingredients.extend(ingredients)

    def get_ingredient_by_name(self, name: str) -> Ingredient:
        return next((ing for ing in self.__ingredients if ing.name == name), None)

    def get_ingredients_by_category(self, category: str) -> List[Ingredient]:
        return [ing for ing in self.__ingredients if ing.category.name == category]

    def get_all_ingredients(self) -> List[Ingredient]:
        return sorted(self.__ingredients)

    def sort_ingredients_by_name(self, name: str):
        items = []
        for ing in self.__ingredients:
            if name.lower() in ing.name.lower():
                items.append(ing)
        return sorted(items, key=lambda ing: ing.name)

    def sort_ingredients_by_category(self, category: str):
        items = []
        for ing in self.__ingredients:
            for cat in ing.categories:
                if category.lower() in cat.name.lower():
                    items.append(ing)
        return sorted(items, key=lambda ing: ing.name)

    def add_category(self, category: Category):
        self.__categories.append(category)

    def add_multiple_categories(self, categories: List[Category]):
        self.__categories.extend(categories)

    def get_category_by_name(self, name: str) -> Category:
        return next((cat for cat in self.__categories if cat.name == name), None)

    def get_all_categories(self) -> List[Category]:
        return self.__categories

    def add_user(self, user: User):
        self.__users.append(user)

    def get_user_by_username(self, username: str) -> User:
        return next((u for u in self.__users if u.username == username), None)

    def get_all_users(self) -> List[User]:
        return self.__users

    def get_total_user_size(self):
        return len(self.__users)

    def create_user(self, username: str, email: str, password_hash: str) -> User:
        return User(self.get_total_user_size() + 1, username, email, password_hash)

    def get_user_by_email(self, email_clean: str) -> User:
        return next((u for u in self.__users if u.email == email_clean), None)

    def get_user_saved_recipes(self, user):
        return user.saved_recipes

    def add_saved_recipe(self, recipe, user):
        user.save_recipe(recipe)

    def user_has_saved_recipe(self, recipe, user):
        return recipe in user.saved_recipes

    def remove_saved_recipe(self, recipe, user):
        user.remove_saved_recipe(recipe)

    def get_user_recipe_ingredients_by_recipe_name(self, user, recipe_name):
        return user.recipe_ingredients.get(recipe_name, [])

    def add_user_recipe_ingredient(self, user, recipe_name, ingredient_string):
        user.add_recipe_ingredient(recipe_name, ingredient_string)

    def remove_user_recipe_ingredient(self, user, recipe_name, ingredient_string):
        user.remove_recipe_ingredient(recipe_name, ingredient_string)

    def add_multiple_user_recipe_ingredients(
        self, user, recipe_name, ingredient_strings: List
    ):
        user.add_multiple_recipe_ingredients(recipe_name, ingredient_strings)

    def remove_multiple_user_recipe_ingredients(
        self, user, recipe_name, ingredient_strings: List
    ):
        user.remove_recipe_ingredients(recipe_name, ingredient_strings)

    def clear_user_recipe_ingredients(self, user, recipe_name):
        user.clear_recipe_ingredients_by_recipe(recipe_name)

    def delete_user_recipe_ingredients_per_recipe(self, user, recipe_name):
        user.delete_recipe_ingredients_per_recipe(recipe_name)

    def clear_recipe_ingredients(self, user):
        user.clear_all_recipe_ingredients()

    def update_user(self, user: User):
        for idx, existing_user in enumerate(self.__users):
            if existing_user.id == user.id:
                self.__users[idx] = user
                return
        raise RepositoryException(f"User with id {user.id} not found.")

    def add_recipe(self, recipe: recipe):
        self.__recipes.append(recipe)

    def add_multiple_recipes(self, recipes: List[recipe]):
        self.__recipes.extend(recipes)

    def get_recipe_by_name(self, name: str) -> recipe:
        return next(
            (rec for rec in self.__recipes if rec.name.lower() == name.lower()), None
        )

    def get_recipes_by_category(self, category: str) -> List:
        return [rec for rec in self.__recipes if rec.category == category]

    def get_all_recipes(self) -> List[recipe]:
        return sorted(self.__recipes)

    def sort_recipes_by_name(self, name: str):
        items = []
        for rec in self.__recipes:
            if name.lower() in rec.name.lower():
                items.append(rec)
        return sorted(items, key=lambda rec: rec.name)

    def sort_recipes_by_category(self, category: str):
        items = []
        for rec in self.__recipes:
            if category.lower() in rec.category.lower():
                items.append(rec)
        return sorted(items, key=lambda rec: rec.name)
