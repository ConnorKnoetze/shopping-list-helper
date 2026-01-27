def test_datareader_parses_files():
    from pantry.adapters.datareader.reader import DataReader
    from pantry.domainmodel.category import Category

    reader = DataReader()

    # must have categories and ingredients
    cats = reader.categories
    ings = reader.ingredients
    recs = reader.recipes

    assert isinstance(cats, set)
    assert isinstance(ings, set)
    assert isinstance(recs, set)

    # pick some expected ingredient from CSV
    names = {ing.name for ing in ings}
    assert "Carrot" in names

    # categories are Category instances
    assert any(isinstance(c, Category) for c in cats)

    # recipes should be Recipe instances and contain ids
    from pantry.domainmodel.recipe import Recipe

    assert any(isinstance(r, Recipe) for r in recs)
