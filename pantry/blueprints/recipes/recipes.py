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
