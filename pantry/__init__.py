from dotenv import load_dotenv
from flask import render_template
from sqlalchemy import create_engine, NullPool, inspect
from sqlalchemy.orm import sessionmaker, clear_mappers

from pantry.adapters import repository
from pantry.adapters.memory_repository import MemoryRepository
from pantry.adapters.populate_repository import populate
from pantry.blueprints.authentication.authentication import authentication_blueprint
from pantry.blueprints.home.home import home_bp
from pantry.blueprints.inventory.inventory import inventory_bp
from pantry.blueprints.recipes.recipes import recipes_bp
from pantry.blueprints.shopping.shopping import shopping_bp
from pantry.blueprints.user.user import user_bp
from pantry.utilities.auth import get_current_user

from pantry.blueprints.services import _repo

from pantry.adapters.database_repository import SqlAlchemyRepository

def create_app():
    from flask import Flask

    load_dotenv()
    app = Flask(__name__)
    app.config.from_object("config.Config")

    if app.config["REPOSITORY"] == "memory":
        repository.repo_instance = MemoryRepository()
        populate(_repo())

    elif app.config["REPOSITORY"] == "database":
        database_uri = app.config["SQLALCHEMY_DATABASE_URI"]

        database_echo = app.config["SQLALCHEMY_ECHO"]
        if database_uri.startswith("sqlite"):
            database_engine = create_engine(
                database_uri,
                connect_args={"check_same_thread": False},
                poolclass=NullPool,
                echo=database_echo,
            )
        else:
            database_engine = create_engine(
                database_uri,
                pool_size=5,
                max_overflow=10,
                pool_pre_ping=True,
                echo=database_echo,
            )

        session_factory = sessionmaker(
            autocommit=False, autoflush=True, bind=database_engine
        )

        inspector = inspect(database_engine)

        clear_mappers()
        from pantry.adapters import orm as orm

        if len(inspector.get_table_names()) == 0:
            print("No tables found — creating tables and populating database...")
            orm.Base.metadata.create_all(database_engine)
            repository.repo_instance = SqlAlchemyRepository(session_factory, database_uri)
            database_mode = True
            populate(repository.repo_instance, database_mode)
        else:
            print("Tables found")
            repository.repo_instance = SqlAlchemyRepository(session_factory, database_uri)

    app.register_blueprint(home_bp)
    app.register_blueprint(authentication_blueprint)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(recipes_bp)
    app.register_blueprint(shopping_bp)
    app.register_blueprint(user_bp)

    @app.context_processor
    def inject_user():
        return {"current_user": get_current_user()}

    return app
