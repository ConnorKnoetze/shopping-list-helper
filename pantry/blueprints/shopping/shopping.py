import os
from pathlib import Path

from flask import render_template, Blueprint, session

from pantry.blueprints.authentication.authentication import login_required

from pantry.blueprints.services import _repo

PROJECT_ROOT = Path(__file__).parent.parent.parent

DOWNLOADS_PATH = PROJECT_ROOT / "static" / "downloads"

shopping_bp = Blueprint("shopping", __name__)


@shopping_bp.route("/shopping")
@login_required
def shopping():
    repo = _repo()
    username = session.get("username")
    user = repo.get_user_by_username(username)

    grocery_list = user.grocery_list if user else []

    print(user.recipe_ingredients)
    # Pass the variable name expected by the template
    return render_template(
        "pages/shopping/shopping.html",
        grocery_items=grocery_list,
        saved_recipes=user.saved_recipes,
        recipe_ingredients=user.recipe_ingredients,
    )


@shopping_bp.route("/shopping/api/remove/<string:name>", methods=["POST"])
@login_required
def remove_from_shopping_api(name: str):
    from flask import jsonify

    repo = _repo()
    username = session.get("username")
    user = repo.get_user_by_username(username)

    ing = repo.get_ingredient_by_name(name)

    if ing in user.grocery_list:
        user.grocery_list.remove(ing)
        repo.update_user(user)
        return jsonify(
            {
                "success": True,
                "message": f"{name} removed from grocery list.",
                "name": name,
            }
        ), 200
    else:
        return jsonify(
            {
                "success": False,
                "message": f"{name} not found in grocery list.",
                "name": name,
            }
        ), 404


@shopping_bp.route("/shopping/api/download", methods=["GET"])
@login_required
def download_shopping_list_api():
    from flask import jsonify

    repo = _repo()
    username = session.get("username")
    user = repo.get_user_by_username(username)

    grocery_list = user.grocery_list if user else []

    shopping_list_text = "Grocery List:\n\n"
    for item in grocery_list:
        shopping_list_text += f"- {item.name}: {item.quantity} {item.unit}\n"

    return jsonify({"shopping_list": shopping_list_text}), 200
