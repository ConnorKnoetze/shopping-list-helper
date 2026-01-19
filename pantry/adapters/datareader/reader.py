from pathlib import Path
import csv

from pantry.domainmodel.category import Category
from pantry.domainmodel.ingredient import Ingredient

PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_FILE = PROJECT_ROOT / 'adapters' / 'data' /'ingredients.csv'

class DataReader:
    def __init__(self, file_path=DATA_FILE):
        self.file_path = file_path
        self.__categories = set()
        self.__ingredients = set()
        self.read_data()

    def read_data(self):
        with open(self.file_path, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                ingredient_name = row["ingredient"].strip()
                categories = [Category(c.strip()) for c in row['categories'].strip().split(";")]
                unit = row['unit'].strip()

                range_min = int(row['range_min'].strip())
                range_max = int(row['range_max'].strip())
                step = int(row['step'].strip())

                ingredient = Ingredient(name=ingredient_name, quantity=0, unit=unit, categories=categories, range_min=range_min, range_max=range_max, step=step)

                for category in categories:
                    self.__categories.add(category)
                self.__ingredients.add(ingredient)

    @property
    def categories(self):
        return self.__categories

    @property
    def ingredients(self):
        return self.__ingredients

if __name__ == "__main__":
    reader = DataReader()

    print("Categories:")
    for category in reader.categories:
        print(category)

    print("\nIngredients:")
    for ingredient in reader.ingredients:
        print(ingredient)
