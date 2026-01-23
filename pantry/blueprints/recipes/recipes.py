from flask import render_template, Blueprint

from pantry.adapters import repository
from pantry.blueprints.authentication.authentication import login_required

recipes_bp = Blueprint("recipes_bp", __name__)


@recipes_bp.route("/recipes")
@login_required
def recipes():
    repo = repository.repo_instance

    recipes = repo.get_all_recipes()

    return render_template("pages/recipes/recipes.html", recipes=recipes)

@recipes_bp.route("/recipes/<string:recipe_name>")
@login_required
def recipe_detail(recipe_name):
    repo = repository.repo_instance

    handled_recipe = " ".join(recipe_name.split('-'))

    recipe = repo.get_recipe_by_name(handled_recipe)

    if not recipe:
        return render_template("pages/errors/404.html"), 404

    return render_template("pages/recipes/recipe-detail.html", recipe=recipe)