from typing import List, Tuple, Dict, Any

from wtforms.validators import none_of

from pantry.domainmodel.ingredient import Ingredient


class User:
    def __init__(
        self, user_id: int, username: str, email: str, password_hash: str = None
    ):
        self.__user_id = user_id
        self.__username = username
        self.__email = email
        self.__password_hash = password_hash
        self.__grocery_list: List[Ingredient] = []
        self.__recipe_ingredients: Dict[str : List[str]] = {}
        self.__saved_recipes: List[int] = []

    def __repr__(self):
        return f"User(user_id={self.id}, username='{self.username}', email='{self.email}', grocery_list={self.grocery_list}')"

    @property
    def id(self):
        return self.__user_id

    @property
    def username(self):
        return self.__username

    @property
    def email(self):
        return self.__email

    @property
    def password_hash(self):
        return self.__password_hash

    @property
    def grocery_list(self):
        return self.__grocery_list

    @username.setter
    def username(self, username: str):
        self.__username = username

    @email.setter
    def email(self, email: str):
        self.__email = email

    def add_grocery(self, item: Ingredient, quantity: int) -> None:
        ing = item
        ing.quantity = quantity

        for existing_ing in self.__grocery_list:
            if existing_ing == ing:
                existing_ing.quantity += quantity
                return

        self.__grocery_list.append(ing)

    def remove_grocery(self, item: Ingredient) -> None:
        self.__grocery_list = [ing for ing in self.__grocery_list if ing != item]

    @property
    def recipe_ingredients(self) -> dict[Any]:
        return self.__recipe_ingredients

    def add_recipe_ingredient(self, recipe_name ,ingredient_string: str) -> None:
        if recipe_name not in self.__recipe_ingredients:
            self.__recipe_ingredients[recipe_name] = []
        if ingredient_string not in self.__recipe_ingredients[recipe_name]:
            self.__recipe_ingredients[recipe_name].append(ingredient_string)

    def remove_recipe_ingredient(self, recipe_name, ingredient_string: str) -> None:
        if recipe_name in self.__recipe_ingredients:
            self.__recipe_ingredients[recipe_name] = [
                ing for ing in self.__recipe_ingredients[recipe_name] if ing != ingredient_string
            ]
            if not self.__recipe_ingredients[recipe_name]:
                del self.__recipe_ingredients[recipe_name]

    def add_multiple_recipe_ingredients(self, recipe_name, ingredient_strings: List[str]) -> None:
        if recipe_name not in self.__recipe_ingredients:
            self.__recipe_ingredients[recipe_name] = []
        for string in ingredient_strings:
            if string not in self.__recipe_ingredients[recipe_name]:
                self.__recipe_ingredients[recipe_name].append(string)

    def remove_multiple_recipe_ingredients(self, recipe,ingredient_strings: List[str]) -> None:
        if recipe in self.__recipe_ingredients:
            self.__recipe_ingredients[recipe] = [
                ing for ing in self.__recipe_ingredients[recipe] if ing not in ingredient_strings
            ]
            if not self.__recipe_ingredients[recipe]:
                del self.__recipe_ingredients[recipe]

    def clear_recipe_ingredients_by_recipe(self, recipe_name) -> None:
        if recipe_name in self.__recipe_ingredients:
            del self.__recipe_ingredients[recipe_name]

    def delete_recipe_ingredients_per_recipe(self, recipe_name):
        lowered_name = recipe_name.lower()
        if lowered_name in self.recipe_ingredients:
            del self.recipe_ingredients[lowered_name]

    def clear_all_recipe_ingredients(self) -> None:
        self.__recipe_ingredients = {}

    @property
    def saved_recipes(self):
        return self.__saved_recipes

    def save_recipe(self, recipe_id: int):
        if recipe_id not in self.__saved_recipes:
            self.__saved_recipes.append(recipe_id)

    def remove_saved_recipe(self, recipe_id: int):
        self.__saved_recipes = [rid for rid in self.__saved_recipes if rid != recipe_id]
