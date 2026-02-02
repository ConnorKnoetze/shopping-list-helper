from flask import render_template, Blueprint, request, session

from pantry.blueprints.authentication.authentication import login_required
from pantry.blueprints.recipes.services import _handle_recipe_ingredients_form

from pantry.blueprints.services import _repo

recipes_bp = Blueprint("recipes_bp", __name__)


@recipes_bp.route("/recipes")
@login_required
def recipes():
    """
    Route for displaying all recipes.
    :return:
        Page template for recipes with context including:
        - recipes: List of all recipe objects retrieved from the repository.
    """

    repo = _repo()

    recipes = repo.get_all_recipes()

    return render_template("pages/recipes/recipes.html", recipes=recipes)


@recipes_bp.route("/recipes/<string:recipe_name>", methods=["GET", "POST"])
@login_required
def recipe_detail(recipe_name):
    """
        Route for displaying the details of a specific recipe and handling ingredient selection.
    :param recipe_name:
    :return:
        Page template for recipe details with context including:
        - recipe: The recipe object retrieved from the repository.
        - ingredients: List of ingredients for the recipe.
        - selected_ingredients: List of ingredients selected by the user.
        - saved: Boolean indicating if the recipe is saved by the user.
    404 Not Found if the recipe does not exist.
    """
    selected_ingredients = []
    username = session.get("username")
    repo = _repo()
    user = repo.get_user_by_username(username)
    selected = request.form.getlist("ingredients[]")

    handled_recipe = " ".join(recipe_name.split("-"))
    if request.method == "POST":
        selected_ingredients = _handle_recipe_ingredients_form(
            selected, user, handled_recipe, repo
        )

    recipe = repo.get_recipe_by_name(handled_recipe)

    if not recipe:
        return render_template("pages/errors/404.html"), 404

    try:
        user_ingredients = user.recipe_ingredients[handled_recipe]
    except KeyError:
        user_ingredients = []

    if not selected_ingredients and user_ingredients:
        selected_ingredients = [ingredient[2] for ingredient in user_ingredients]

    saved_flag = repo.user_has_saved_recipe(recipe, user)

    return render_template(
        "pages/recipes/recipe-detail.html",
        recipe=recipe,
        ingredients=recipe.ingredients,
        selected_ingredients=selected_ingredients,
        saved=saved_flag,
    )


@recipes_bp.route("/recipes/toggle_save/<string:recipe_name>", methods=["POST"])
@login_required
def toggle_save_recipe(recipe_name):
    """
        API endpoint to toggle saving a recipe for the logged-in user.
        If the recipe is already saved, it will be removed from the user's saved recipes.
        If not, it will be added. And the repository will be updated accordingly.
    Args:
        recipe_name (str): The name of the recipe to toggle save status for.
    Returns:
        dict: A JSON response containing:
        "saved": <bool>,  # True if the recipe is now saved, False if removed

        "recipe_name": <str>  # The recipe name matched to the URL format (lowercase, hyphen-separated)
    200 OK on success, 404 Not Found if the recipe does not exist.
    """
    username = session.get("username")
    repo = _repo()
    user = repo.get_user_by_username(username)
    recipe = repo.get_recipe_by_name(" ".join(recipe_name.split("-")))

    if not recipe:
        return render_template("pages/errors/404.html"), 404

    if repo.user_has_saved_recipe(recipe, user):
        repo.remove_saved_recipe(recipe, user)
        repo.delete_user_recipe_ingredients_per_recipe(user, recipe.name)
        saved = False
    else:
        repo.add_saved_recipe(recipe, user)
        saved = True

    repo.update_user(user)

    return {
        "saved": saved,
        "recipe_name": "-".join(recipe.name.lower().split(" ")),
    }, 200
