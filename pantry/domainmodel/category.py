class Category:
    def __init__(self, name: str):
        self.__name = name

    def __repr__(self):
        return f"{self.name}"

    def __eq__(self, other):
        if isinstance(other, Category):
            return self.name == other.name
        return False

    def __hash__(self):
        return hash(self.name)

    @property
    def name(self):
        return self.__name
