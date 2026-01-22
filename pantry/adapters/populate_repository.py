from pantry.adapters.datareader.reader import DataReader


def populate(repo, database_mode: bool = False):
    data_reader = DataReader()

    if database_mode:
        # Database mode: add data via repository methods
        print("populating categories...")
        repo.add_multiple_categories(data_reader.categories)
        print("done populating categories")
        print("populating ingredients...")
        repo.add_multiple_ingredients(data_reader.ingredients)
        print("done populating ingredients")
    else:
        # Memory mode: simple population
        print("populating categories...")
        repo.add_multiple_categories(data_reader.categories)
        print("done populating categories")
        print("populating ingredients...")
        repo.add_multiple_ingredients(data_reader.ingredients)
        print("done populating ingredients")
        print("populating recipes...")
        repo.add_multiple_recipes(data_reader.recipes)
        print("done populating recipes")
