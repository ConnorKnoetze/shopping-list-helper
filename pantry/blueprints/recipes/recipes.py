from flask import render_template, Blueprint, request, session

from pantry.blueprints.authentication.authentication import login_required
from pantry.blueprints.recipes.services import _handle_recipe_ingredients_form

from pantry.blueprints.services import _repo

recipes_bp = Blueprint("recipes_bp", __name__)


@recipes_bp.route("/recipes")
@login_required
def recipes():
    repo = _repo()

    recipes = repo.get_all_recipes()

    return render_template("pages/recipes/recipes.html", recipes=recipes)


@recipes_bp.route("/recipes/<string:recipe_name>", methods=["GET", "POST"])
@login_required
def recipe_detail(recipe_name):
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
        selected_ingredients = user_ingredients

    print(repo.get_user_by_username(username).recipe_ingredients, repo.get_user_by_username(username).saved_recipes)

    return render_template(
        "pages/recipes/recipe-detail.html",
        recipe=recipe,
        ingredients=recipe.ingredients,
        selected_ingredients=selected_ingredients,
        saved=recipe in user.saved_recipes
    )


@recipes_bp.route("/recipes/toggle_save/<string:recipe_name>", methods=["POST"])
@login_required
def toggle_save_recipe(recipe_name):
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

    print(user.recipe_ingredients, user.saved_recipes, saved)

    return {"saved": saved}