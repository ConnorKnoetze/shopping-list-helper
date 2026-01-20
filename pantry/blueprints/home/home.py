from flask import render_template, Blueprint

from pantry.adapters import repository
from pantry.blueprints.authentication.authentication import login_required

home_bp = Blueprint("home_bp", __name__)

@home_bp.route("/")
@login_required
def home():
    repo = repository.repo_instance

    ing = repo.get_all_ingredients()[:10]

    return render_template("pages/home/home.html", ingredients=ing)