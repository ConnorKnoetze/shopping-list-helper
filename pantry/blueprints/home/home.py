from flask import render_template, Blueprint

from pantry.blueprints.authentication.authentication import login_required

from pantry.blueprints.services import _repo

home_bp = Blueprint("home_bp", __name__)


@home_bp.route("/")
def home():
    repo = _repo()

    ing = repo.get_all_ingredients()[:10]

    return render_template("pages/home/home.html", ingredients=ing)
