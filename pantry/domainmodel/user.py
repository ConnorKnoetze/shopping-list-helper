from typing import List

from pantry.domainmodel.ingredient import Ingredient


class User:
    def __init__(self, user_id: int, username: str, email: str, password_hash: str = None):
        self.__user_id = user_id
        self.__username = username
        self.__email = email
        self.__password_hash = password_hash
        self.__grocery_list: List[Ingredient] = []

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

    def add_grocery(self, item: Ingredient, quantity: int):
        ing = item
        ing.quantity = quantity

        for existing_ing in self.__grocery_list:
            if existing_ing == ing:
                existing_ing.quantity += quantity
                return

        self.__grocery_list.append(ing)