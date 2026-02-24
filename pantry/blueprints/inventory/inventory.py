from flask import render_template, Blueprint, request, session

from pantry.blueprints.authentication.authentication import login_required, admin_required

from pantry.blueprints.services import _repo
from pantry.domainmodel.category import Category
from pantry.domainmodel.ingredient import Ingredient

inventory_bp = Blueprint("inventory_bp", __name__)


@inventory_bp.route("/inventory", methods=["GET", "POST"])
@login_required
def inventory():
    repo = _repo()
    param = ""
    criteria = "name"
    inventory_items = []

    user = repo.get_user_by_username(session.get("username"))
    admin = user.admin if user else False

    if request.method == "GET":
        inventory_items = repo.get_all_ingredients()

    elif request.method == "POST":
        param = request.form.get("p", "")
        criteria = request.form.get("c", "name")

        if criteria == "name":
            inventory_items = repo.sort_ingredients_by_name(param)
        elif criteria == "category":
            inventory_items = repo.sort_ingredients_by_category(param)
        else:
            inventory_items = repo.get_all_ingredients()

    return render_template(
        "pages/inventory/inventory.html",
        inventory_items=inventory_items,
        search_param=param,
        search_criteria=criteria,
        admin=admin
    )


@inventory_bp.route("/inventory/api/<string:name>")
@login_required
def inventory_api(name: str):
    from flask import jsonify

    repo = _repo()
    ingredient = repo.get_ingredient_by_name(name)
    if ingredient:
        categories_str = ""
        if ingredient.categories:
            if isinstance(ingredient.categories, list):
                categories_str = ";".join(
                    [
                        cat.name if hasattr(cat, "name") else str(cat)
                        for cat in ingredient.categories
                    ]
                )
            else:
                categories_str = str(ingredient.categories)

        return jsonify(
            {
                "name": ingredient.name,
                "categories": categories_str,
                "unit": ingredient.unit,
                "quantity": ingredient.quantity,
                "range_min": ingredient.range_min,
                "range_max": ingredient.range_max,
                "step": ingredient.step,
            }
        ), 200
    else:
        return jsonify({"error": "Ingredient not found"}), 404


@inventory_bp.route("/inventory/update/<string:name>", methods=["POST"])
@login_required
def update_inventory(name: str):
    from flask import jsonify
    import json

    repo = _repo()
    username = session.get("username")

    if not username:
        return jsonify({"success": False, "message": "User not authenticated"}), 401

    try:
        if request.is_json:
            data = request.get_json()
        else:
            if request.data:
                try:
                    data = json.loads(request.data)
                except json.JSONDecodeError:
                    data = None
            else:
                data = None

        if data is None:
            return jsonify({"success": False, "message": "Invalid JSON data"}), 400

        raw_quantity = data.get("quantity", None)
        unit = data.get("unit", "")

        try:
            quantity = int(raw_quantity)
        except (TypeError, ValueError):
            return jsonify(
                {"success": False, "message": "Quantity must be a number"}
            ), 400

        if quantity < 0:
            return jsonify(
                {"success": False, "message": "Quantity cannot be negative"}
            ), 400

        user = repo.get_user_by_username(username)
        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404

        ingredient = repo.get_ingredient_by_name(name)
        if not ingredient:
            return jsonify({"success": False, "message": "Ingredient not found"}), 404

        if unit and unit != ingredient.unit:
            return jsonify({"success": False, "message": "Invalid unit"}), 400

        user.add_grocery(ingredient, quantity)
        repo.update_user(user)

        return jsonify(
            {
                "success": True,
                "message": f"Successfully added {quantity} {unit} of {name}",
                "item": {"name": name, "quantity": quantity, "unit": unit},
            }
        ), 200

    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {str(e)}")
        return jsonify(
            {"success": False, "message": f"Invalid JSON format: {str(e)}"}
        ), 400

    except Exception as e:
        print(f"Exception: {str(e)}")
        import traceback

        traceback.print_exc()
        return jsonify(
            {"success": False, "message": f"Error updating quantity: {str(e)}"}
        ), 400


@inventory_bp.route("/inventory/api/add", methods=["POST"])
@admin_required
def add_ingredient_api():
    from flask import jsonify
    import json

    repo = _repo()

    try:
        if request.is_json:
            data = request.get_json()
        else:
            if request.data:
                try:
                    data = json.loads(request.data)
                except json.JSONDecodeError:
                    data = None
            else:
                data = None

        if data is None:
            return jsonify({"success": False, "message": "Invalid JSON data"}), 400

        print(data.get("category", ""))

        name = data.get("name", "").strip()
        unit = data.get("unit", "").strip()
        categories = [Category(name) for name in data.get("category", "").split(",")]
        range_min = data.get("range-min", None)
        range_max = data.get("range-max", None)
        step = data.get("step", None)

        print(name, unit, categories, range_min, range_max, step)

        if not name or not unit:
            return jsonify(
                {"success": False, "message": "Name and unit are required"}
            ), 400

        existing_ingredient = repo.get_ingredient_by_name(name)
        if existing_ingredient:
            return jsonify(
                {"success": False, "message": "Ingredient with this name already exists"}
            ), 400

        new_ingredient = repo.add_ingredient(
            Ingredient(
                name=name,
                unit=unit,
                quantity=0,
                categories=categories,
                range_min=range_min,
                range_max=range_max,
                step=step,
            )
        )

        return jsonify(
            {
                "success": True,
                "message": f"Successfully added ingredient {name}",
                "ingredient": {
                    "name": new_ingredient.name,
                    "unit": new_ingredient.unit,
                    "categories": [
                        cat.name if hasattr(cat, "name") else str(cat)
                        for cat in new_ingredient.categories
                    ],
                    "range_min": new_ingredient.range_min,
                    "range_max": new_ingredient.range_max,
                    "step": new_ingredient.step,
                },
            }
        ), 201

    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {str(e)}")
        return jsonify(
            {"success": False, "message": f"Invalid JSON format: {str(e)}"}
        ), 400

    except Exception as e:
        print(f"Exception: {str(e)}")
        import traceback

        traceback.print_exc()
        return jsonify(
            {"success": False, "message": f"Error adding ingredient: {str(e)}"}
        ), 400