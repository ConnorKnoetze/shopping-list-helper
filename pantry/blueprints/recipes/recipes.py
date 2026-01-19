from flask import render_template, Blueprint

from pantry.blueprints.authentication.authentication import login_required

recipes_bp = Blueprint("recipes_bp", __name__)

@recipes_bp.route("/recipes")
@login_required
def recipes():
    return render_template("pages/recipes/recipes.html")