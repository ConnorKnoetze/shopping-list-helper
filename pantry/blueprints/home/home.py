from flask import render_template, Blueprint

from pantry.blueprints.authentication.authentication import login_required

home_bp = Blueprint("home_bp", __name__)

@home_bp.route("/")
@login_required
def home():
    return render_template("pages/home/home.html")