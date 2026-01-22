from typing import List

from pantry.domainmodel.ingredient import Ingredient


class Recipe:
    def __init__(
        self,
        id: int,
        name: str,
        description: str,
        ingredients: List[Ingredient],
        methods: List[str],
        prep_time_mins: int,
        cook_time_mins: int,
        total_time_mins: int,
        difficulty: str,
        category: str,
        cuisine: str,
        tags: List[str],
        notes: str,
        image_url: str,
    ):
        self.__id = id
        self.__name = name
        self.__description = description
        self.__ingredients = ingredients
        self.__methods = methods
        self.__prep_time_mins = prep_time_mins
        self.__cook_time_mins = cook_time_mins
        self.__total_time_mins = total_time_mins
        self.__difficulty = difficulty
        self.__category = category
        self.__cuisine = cuisine
        self.__tags = tags
        self.__notes = notes
        self.__image_url = image_url

    def __repr__(self):
        return f"Recipe(name={self.name}, ingredients={self.ingredients})"

    def __eq__(self, other):
        if not isinstance(other, Recipe):
            return False
        return self.id == other.id and self.name == other.name

    def __hash__(self):
        return hash((self.id, self.name))

    def __lt__(self, other):
        if not isinstance(other, Recipe):
            return NotImplemented
        return self.name < other.name

    @property
    def id(self) -> int:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def description(self) -> str:
        return self.__description
    @property
    def ingredients(self) -> List[Ingredient]:
        return self.__ingredients

    @property
    def methods(self) -> List[str]:
        return self.__methods

    @property
    def prep_time_mins(self) -> int:
        return self.__prep_time_mins

    @property
    def cook_time_mins(self) -> int:
        return self.__cook_time_mins

    @property
    def total_time_mins(self) -> int:
        return self.__total_time_mins

    @property
    def difficulty(self) -> str:
        return self.__difficulty

    @property
    def category(self) -> str:
        return self.__category

    @property
    def cuisine(self) -> str:
        return self.__cuisine

    @property
    def tags(self) -> List[str]:
        return self.__tags

    @property
    def notes(self) -> str:
        return self.__notes

    @property
    def image_url(self) -> str:
        return self.__image_url
