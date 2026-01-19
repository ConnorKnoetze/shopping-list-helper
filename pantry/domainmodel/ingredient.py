class Ingredient:
    def __init__(self, name: str, quantity: float, unit: str, categories=None, range_min=1, range_max=100, step=1):
        self.__name = name
        self.__quantity = quantity
        self.__unit = unit
        self.__categories = categories
        self.__range_min = range_min
        self.__range_max = range_max
        self.__step = step

    def __repr__(self):
        return f"Ingredient(name={self.name}, quantity={self.quantity}, unit={self.unit}, category={self.categories})"

    def __eq__(self, other):
        if isinstance(other, Ingredient):
            return (self.name == other.name and
                    self.quantity == other.quantity and
                    self.unit == other.unit and
                    self.categories == other.categories)
        return False

    def __lt__(self, other):
        return self.name < other.name

    def __hash__(self):
        return hash((self.name, self.quantity, self.unit))

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name: str):
        self.__name = name

    @property
    def quantity(self):
        return self.__quantity

    @quantity.setter
    def quantity(self, quantity: float):
        self.__quantity = quantity

    @property
    def unit(self):
        return self.__unit

    @unit.setter
    def unit(self, unit: str):
        self.__unit = unit

    @property
    def categories(self):
        return self.__categories

    @categories.setter
    def categories(self, categories):
        self.__categories = categories

    @property
    def range_min(self):
        return self.__range_min

    @range_min.setter
    def range_min(self, value):
        self.__range_min = value

    @property
    def range_max(self):
        return self.__range_max

    @range_max.setter
    def range_max(self, value):
        self.__range_max = value

    @property
    def step(self):
        return self.__step

    @step.setter
    def step(self, value):
        self.__step = value