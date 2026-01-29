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

    shopping_list_text = "General Grocery List:\n\n"
    for item in grocery_list:
        shopping_list_text += f"    - {item.name}: {item.quantity} {item.unit}\n"

    user_saved_recipes = user.saved_recipes
    user_recipe_ingredients = user.recipe_ingredients

    for recipe in user_saved_recipes:
        shopping_list_text += f"\n\n{recipe.name}:\n\n"
        for ingredient_tuple in user_recipe_ingredients[recipe.name.lower()]:
            shopping_list_text += f"    - {ingredient_tuple[2]}: {ingredient_tuple[0]} {ingredient_tuple[1]}\n"

    return jsonify({"shopping_list": shopping_list_text}), 200


@shopping_bp.route("/shopping/api/delete_recipe/<string:recipe_name>", methods=["GET", "POST"])
@login_required
def delete_recipe_from_shopping_api(recipe_name: str):
    from flask import jsonify

    repo = _repo()
    username = session.get("username")
    user = repo.get_user_by_username(username)

    recipe_to_delete = None
    for recipe in user.saved_recipes:
        if recipe.name == recipe_name:
            recipe_to_delete = recipe
            break

    if recipe_to_delete:
        user.saved_recipes.remove(recipe_to_delete)
        # Also remove associated ingredients from grocery list
        for ingredient in recipe_to_delete.ingredients:
            if ingredient in user.grocery_list:
                user.grocery_list.remove(ingredient)
        repo.update_user(user)
        return jsonify(
            {
                "success": True,
                "message": f"Recipe '{recipe_name}' and its ingredients removed from grocery list.",
                "recipe_name": recipe_name,
            }
        ), 200
    else:
        return jsonify(
            {
                "success": False,
                "message": f"Recipe '{recipe_name}' not found in saved recipes.",
                "recipe_name": recipe_name,
            }
        ), 404

@shopping_bp.route("/shopping/api/remove_saved_recipe_ingredient/<string:recipe_name>/<string:ingredient_name>", methods=["POST"])
@login_required
def remove_saved_recipe_ingredient_api(recipe_name: str, ingredient_name: str):
    from flask import jsonify

    repo = _repo()
    username = session.get("username")
    user = repo.get_user_by_username(username)

    try:
        user.remove_recipe_ingredient(recipe_name, ingredient_name)
    except Exception as e:
        return jsonify(
            {
                "success": False,
                "message": str(e),
                "ingredient_name": ingredient_name,
                "recipe_name": recipe_name,
            }
        ), 400
    repo.update_user(user)

    return jsonify(
        {
            "success": True,
            "message": f"Ingredient '{ingredient_name}' removed from recipe '{recipe_name}' and grocery list.",
            "ingredient_name": ingredient_name,
            "recipe_name": recipe_name,
        }
    ), 200