from dotenv import load_dotenv
from flask import render_template

from pantry.adapters import repository
from pantry.adapters.memory_repository import MemoryRepository
from pantry.adapters.populate_repository import populate
from pantry.blueprints.authentication.authentication import authentication_blueprint
from pantry.blueprints.home.home import home_bp
from pantry.blueprints.inventory.inventory import inventory_bp
from pantry.blueprints.recipes.recipes import recipes_bp
from pantry.blueprints.shopping.shopping import shopping_bp
from pantry.utilities.auth import get_current_user

from pantry.blueprints.services import _repo

def create_app():
    from flask import Flask

    load_dotenv()
    app = Flask(__name__)
    app.config.from_object("config.Config")

    if app.config["REPOSITORY"] == "memory":
        # Create the MemoryRepository implementation for a memory-based repository.
        repository.repo_instance = MemoryRepository()
        populate(_repo())

    # @app.errorhandler(404)
    # def page_not_found(error):
    #     return render_template("/pages/errors/404.html"), 404

    app.register_blueprint(home_bp)
    app.register_blueprint(authentication_blueprint)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(recipes_bp)
    app.register_blueprint(shopping_bp)

    @app.context_processor
    def inject_user():
        return {"current_user": get_current_user()}

    return app
