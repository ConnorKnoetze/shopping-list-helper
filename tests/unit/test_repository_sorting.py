def test_repository_sorting_and_filters(memory_repo):
    # ensure repository has ingredients from populate
    all_ings = memory_repo.get_all_ingredients()
    assert len(all_ings) > 0

    # search by name
    results = memory_repo.sort_ingredients_by_name("Car")
    assert any("car" in ing.name.lower() or "Car" in ing.name for ing in results)

    # search by category
    # pick a category from an ingredient
    sample = all_ings[0]
    cats = sample.categories
    if cats and isinstance(cats, list):
        catname = cats[0].name if hasattr(cats[0], "name") else str(cats[0])
        res2 = memory_repo.sort_ingredients_by_category(catname)
        assert isinstance(res2, list)
