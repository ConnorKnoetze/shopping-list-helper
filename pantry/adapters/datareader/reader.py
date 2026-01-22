from pathlib import Path
import csv

from pantry.domainmodel.category import Category
from pantry.domainmodel.ingredient import Ingredient
from pantry.domainmodel.recipe import Recipe

PROJECT_ROOT = Path(__file__).parent.parent.parent
INGREDIENTS_DATA_FILE = PROJECT_ROOT / 'adapters' / 'data' /'ingredients.csv'
RECIPE_DATA_FILE = PROJECT_ROOT / 'adapters' / 'data' / 'recipes.csv'

class DataReader:
    def __init__(self):
        self.__categories = set()
        self.__ingredients = set()
        self.__recipes = set()
        self.read_data()

    def read_data(self):
        with open(INGREDIENTS_DATA_FILE, mode='r', newline='', encoding='utf-8') as csvfile:
            ingredients_reader = csv.DictReader(csvfile)
            for row in ingredients_reader:
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

        with open(RECIPE_DATA_FILE, mode='r', newline='', encoding='utf-8') as csvfile:
            recipes_reader = csv.DictReader(csvfile)
            for row in recipes_reader:
                recipe_id = int(row["id"].strip())
                recipe_name = row["name"].strip()
                recipe_description = row["description"].strip()
                recipe_ingredients = [ing.strip() for ing in row["ingredients"].strip().split(";")]
                recipe_methods = [method.strip() for method in row["method"].strip().split("||")]
                recipe_prep_time_mins = int(row["prep_time_mins"].strip()) if row["prep_time_mins"].strip() else None
                recipe_cook_time_mins = int(row["cook_time_mins"].strip()) if row["cook_time_mins"].strip() else None
                recipe_total_time_mins = int(row["total_time_mins"].strip()) if row["total_time_mins"].strip() else None
                recipe_difficulty = row["difficulty"].strip()
                recipe_category = row["category"].strip()
                recipe_cuisine = row["cuisine"].strip()
                recipe_tags = [tag.strip() for tag in row["tags"].strip().split(",")]
                recipe_notes = row["notes"]
                recipe_image_url = row["image_url"].strip()

                matching_ingredients = []
                for ingredient in recipe_ingredients:
                    matching_ingredient = next((ing for ing in self.__ingredients if ing.name.lower() in ingredient.lower()), None)
                    matching_ingredients.append(matching_ingredient)

                recipe = Recipe(
                    id=recipe_id,
                    name=recipe_name,
                    description=recipe_description,
                    ingredients=matching_ingredients,
                    methods=recipe_methods,
                    prep_time_mins=recipe_prep_time_mins,
                    cook_time_mins=recipe_cook_time_mins,
                    total_time_mins=recipe_total_time_mins,
                    difficulty=recipe_difficulty,
                    category=recipe_category,
                    cuisine=recipe_cuisine,
                    tags=recipe_tags,
                    notes=recipe_notes,
                    image_url=recipe_image_url
                )
                self.__recipes.add(recipe)

    @property
    def categories(self):
        return self.__categories

    @property
    def ingredients(self):
        return self.__ingredients

    @property
    def recipes(self):
        return self.__recipes

if __name__ == "__main__":
    reader = DataReader()

    print("Categories:")
    for category in reader.categories:
        print(category)

    print("\nIngredients:")
    for ingredient in reader.ingredients:
        print(ingredient)

    print("\nRecipes:")
    for recipe in reader.recipes:
        print(recipe)
