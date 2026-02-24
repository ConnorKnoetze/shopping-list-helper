from typing import List, Tuple, Dict, Any

from wtforms.validators import none_of

from pantry.domainmodel.ingredient import Ingredient


class User:
    def __init__(
        self, user_id: int, username: str, email: str, password_hash: str = None, admin: bool = False
    ):
        self.__user_id = user_id
        self.__username = username
        self.__email = email
        self.__password_hash = password_hash
        self.__grocery_list: List[Ingredient] = []
        self.__recipe_ingredients: Dict[str, List[str]] = {}
        self.__saved_recipes: List[int] = []
        self.__admin = admin

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
    def recipe_ingredients(self) -> Dict[str, List[str]]:
        return self.__recipe_ingredients

    def add_recipe_ingredient(self, recipe_name, ingredient_string: str) -> None:
        found_key = None
        for k in self.__recipe_ingredients.keys():
            if k.lower() == recipe_name.lower():
                found_key = k
                break
        if not found_key:
            found_key = recipe_name
            self.__recipe_ingredients[found_key] = []

        if isinstance(ingredient_string, (list, tuple)) and len(ingredient_string) > 0:
            disp = str(ingredient_string[2]) if len(ingredient_string) > 2 else str(ingredient_string[-1])
        else:
            disp = str(ingredient_string)
        disp_l = disp.lower()

        for existing in self.__recipe_ingredients[found_key]:
            if isinstance(existing, (list, tuple)):
                name = existing[2] if len(existing) > 2 else str(existing[-1])
            else:
                name = str(existing)
            if name.lower() == disp_l:
                return

        self.__recipe_ingredients[found_key].append(ingredient_string)

    def remove_recipe_ingredient(self, recipe_name, ingredient_string: str) -> None:
        found_key = None
        for k in list(self.__recipe_ingredients.keys()):
            if k.lower() == recipe_name.lower():
                found_key = k
                break
        if not found_key:
            return

        target_l = str(ingredient_string).lower()
        def _keep(ing):
            if isinstance(ing, (list, tuple)) and len(ing) > 0:
                name = existing_name = (ing[2] if len(ing) > 2 else str(ing[-1]))
                return name.lower() != target_l
            else:
                return str(ing).lower() != target_l

        self.__recipe_ingredients[found_key] = [ing for ing in self.__recipe_ingredients[found_key] if _keep(ing)]
        if not self.__recipe_ingredients[found_key]:
            del self.__recipe_ingredients[found_key]

    def add_multiple_recipe_ingredients(
        self, recipe_name, ingredient_strings: List[str]
    ) -> None:
        for string in ingredient_strings:
            self.add_recipe_ingredient(recipe_name, string)

    def remove_multiple_recipe_ingredients(
        self, recipe, ingredient_strings: List[str]
    ) -> None:
        found_key = None
        for k in list(self.__recipe_ingredients.keys()):
            if k.lower() == recipe.lower():
                found_key = k
                break
        if not found_key:
            return
        for s in ingredient_strings:
            self.remove_recipe_ingredient(recipe, s)

    def clear_recipe_ingredients_by_recipe(self, recipe_name) -> None:
        for k in list(self.__recipe_ingredients.keys()):
            if k.lower() == recipe_name.lower():
                del self.__recipe_ingredients[k]
                break

    def delete_recipe_ingredients_per_recipe(self, recipe_name):
        self.clear_recipe_ingredients_by_recipe(recipe_name)

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

    @property
    def admin(self):
        return self.__admin