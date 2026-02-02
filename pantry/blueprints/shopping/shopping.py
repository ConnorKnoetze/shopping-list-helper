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
    """
    Renders the shopping list page for the logged-in user.
    :return:
    Rendered shopping list template with grocery items and saved recipes.
    """
    repo = _repo()
    username = session.get("username")
    user = repo.get_user_by_username(username)

    grocery_list = user.grocery_list if user else []

    all_recipes = repo.get_all_recipes()
    recipe_map = {r.id: r for r in all_recipes}
    saved_recipes = [recipe_map[rid] for rid in (user.saved_recipes or []) if rid in recipe_map]

    ri = {}
    for k, v in (user.recipe_ingredients or {}).items():
        ri[k.lower()] = v

    return render_template(
        "pages/shopping/shopping.html",
        grocery_items=grocery_list,
        saved_recipes=saved_recipes,
        recipe_ingredients=ri,
    )


@shopping_bp.route("/shopping/api/remove/<string:name>", methods=["POST"])
@login_required
def remove_from_shopping_api(name: str):

    """
    Removes an ingredient from the user's grocery list.
    :param name:
    :return:
    JSON response indicating success or failure of the removal operation.
    {
        success: bool,
        message: str,
        name: str
    }
    """

    from flask import jsonify

    repo = _repo()
    username = session.get("username")
    user = repo.get_user_by_username(username)

    found = None
    for ing in list(user.grocery_list):
        try:
            if ing.name.lower() == name.lower():
                found = ing
                break
        except Exception:
            continue

    if found:
        user.grocery_list.remove(found)
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

    """Generates and returns the user's shopping list as a downloadable text file.

    Returns JSON containing the shopping list text.
    """

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

    all_recipes = repo.get_all_recipes()
    recipe_map = {r.id: r for r in all_recipes}

    for recipe_id in user_saved_recipes:
        recipe_obj = recipe_map.get(recipe_id)
        if not recipe_obj:
            continue
        shopping_list_text += f"\n\n{recipe_obj.name}:\n\n"
        ri_list = []
        for k, v in (user_recipe_ingredients or {}).items():
            if k.lower() == recipe_obj.name.lower():
                ri_list = v
                break
        for ingr in ri_list:
            shopping_list_text += f"    - {ingr[2]} {ingr[0]} {ingr[1]}\n"

    return jsonify({"shopping_list": shopping_list_text}), 200


@shopping_bp.route("/shopping/api/delete_recipe/<string:recipe_name>", methods=["GET", "POST"])
@login_required
def delete_recipe_from_shopping_api(recipe_name: str):

    """
    Deletes a saved recipe and its associated ingredients from the user's grocery list.
    :param recipe_name:
    :return:
    JSON response indicating success or failure of the deletion operation.
    {
        success: bool,
        message: str,
        recipe_name: str
    }
    """

    from flask import jsonify

    repo = _repo()
    username = session.get("username")
    user = repo.get_user_by_username(username)

    recipe_obj = repo.get_recipe_by_name(recipe_name)
    if not recipe_obj:
        return jsonify({"success": False, "message": f"Recipe '{recipe_name}' not found.", "recipe_name": recipe_name}), 404

    recipe_id = recipe_obj.id

    if recipe_id in user.saved_recipes:
        user.remove_saved_recipe(recipe_id)

        for ingredient in recipe_obj.ingredients:
            ing_name = ingredient[0] if isinstance(ingredient, (list, tuple)) and len(ingredient) > 0 else str(ingredient)
            for g in list(user.grocery_list):
                try:
                    if g.name.lower() == str(ing_name).lower():
                        user.grocery_list.remove(g)
                except Exception:
                    continue

        keys_to_delete = [k for k in (user.recipe_ingredients or {}).keys() if k.lower() == recipe_name.lower()]
        for k in keys_to_delete:
            del user.recipe_ingredients[k]

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

    """
    Removes a specific ingredient associated with a saved recipe from the user's grocery list.
    :param recipe_name:
    :param ingredient_name:
    :return:
    JSON response indicating success or failure of the removal operation.
    {
        success: bool,
        message: str,
        ingredient_name: str,
        recipe_name: str
    }
    """

    from flask import jsonify

    repo = _repo()
    username = session.get("username")
    user = repo.get_user_by_username(username)

    try:
        user.remove_recipe_ingredient(recipe_name, ingredient_name)
        for g in list(user.grocery_list):
            try:
                if g.name.lower() == ingredient_name.lower():
                    user.grocery_list.remove(g)
            except Exception:
                continue
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
