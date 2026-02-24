from abc import ABC
from typing import List, Tuple
from pathlib import Path

from sqlalchemy import func, select, text, inspect
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.exc import NoResultFound

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from pantry.adapters.repository import AbstractRepository


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        # Return the actual Session instance from the scoped_session proxy
        return self.__session()

    def commit(self) -> object:
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if self.__session is not None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session_factory, database_uri: str):
        self._session_cm = SessionContextManager(session_factory)
        self._engine = create_engine(database_uri, future=True)
        self._session_factory = sessionmaker(bind=self._engine, expire_on_commit=False)

        from pantry.adapters import orm as _orm

        self._orm = _orm

    def add_ingredient(self, ingredient):
        session = self._session_cm.session
        ingr_model = self._orm.ensure_ingredient(session, ingredient.name)
        # persist unit and UI range/step values from domain Ingredient
        try:
            if hasattr(ingredient, 'unit') and ingredient.unit is not None:
                ingr_model.unit = ingredient.unit
        except Exception:
            pass
        try:
            if hasattr(ingredient, 'range_min'):
                ingr_model.range_min = int(ingredient.range_min) if ingredient.range_min is not None else ingr_model.range_min
        except Exception:
            pass
        try:
            if hasattr(ingredient, 'range_max'):
                ingr_model.range_max = int(ingredient.range_max) if ingredient.range_max is not None else ingr_model.range_max
        except Exception:
            pass
        try:
            if hasattr(ingredient, 'step'):
                ingr_model.step = int(ingredient.step) if ingredient.step is not None else ingr_model.step
        except Exception:
            pass
        # attach categories if present
        if getattr(ingredient, "categories", None):
            cat = ",".join([str(cate) for cate in ingredient.categories])
            cat_model = self._orm.ensure_category(session, cat if isinstance(cat, str) else cat.name)
            if cat_model not in ingr_model.categories:
                ingr_model.categories.append(cat_model)
        self._session_cm.commit()
        return ingredient

    def add_multiple_ingredients(self, ingredients: List):
        for ing in ingredients:
            self.add_ingredient(ing)

    def get_ingredient_by_name(self, name: str):
        session = self._session_cm.session
        model = session.query(self._orm.IngredientModel).filter_by(name=name).first()
        if not model:
            return None
        return model.to_domain()

    def get_ingredients_by_category(self, category: str) -> List:
        session = self._session_cm.session
        cat = session.query(self._orm.CategoryModel).filter(func.lower(self._orm.CategoryModel.name) == category.lower()).first()
        if not cat:
            return []
        return [ing.to_domain() for ing in cat.ingredients]

    def get_all_ingredients(self) -> List:
        session = self._session_cm.session
        models = session.query(self._orm.IngredientModel).all()
        return sorted([m.to_domain() for m in models], key=lambda i: i.name)

    def sort_ingredients_by_name(self, name: str):
        session = self._session_cm.session
        # case-insensitive contains
        models = (
            session.query(self._orm.IngredientModel)
            .filter(func.lower(self._orm.IngredientModel.name).contains(name.lower()))
            .order_by(self._orm.IngredientModel.name)
            .all()
        )
        return [m.to_domain() for m in models]

    def sort_ingredients_by_category(self, category: str):
        session = self._session_cm.session
        # find categories that match then collect unique ingredients
        cats = (
            session.query(self._orm.CategoryModel)
            .filter(func.lower(self._orm.CategoryModel.name).contains(category.lower()))
            .all()
        )
        ingredients = set()
        for c in cats:
            for ing in c.ingredients:
                ingredients.add(ing)
        return sorted([ing.to_domain() for ing in ingredients], key=lambda i: i.name)

    def add_category(self, category):
        session = self._session_cm.session
        self._orm.ensure_category(session, category.name if not isinstance(category, str) else category)
        self._session_cm.commit()

    def add_multiple_categories(self, categories: List):
        for c in categories:
            self.add_category(c)

    def get_category_by_name(self, name: str):
        session = self._session_cm.session
        model = session.query(self._orm.CategoryModel).filter(func.lower(self._orm.CategoryModel.name) == name.lower()).first()
        if not model:
            return None
        return model.to_domain()

    def get_all_categories(self) -> List:
        session = self._session_cm.session
        models = session.query(self._orm.CategoryModel).all()
        return [m.to_domain() for m in models]

    def add_user(self, user):
        session = self._session_cm.session
        # accept either domain User or UserModel
        if hasattr(user, "id") and not isinstance(user, self._orm.UserModel):
            self._orm.user_from_domain(session, user)
        else:
            session.add(user)
        self._session_cm.commit()

    def get_user_by_username(self, username: str):
        session = self._session_cm.session
        model = session.query(self._orm.UserModel).filter(func.lower(self._orm.UserModel.username) == username.lower()).first()
        if not model:
            return None
        return model.to_domain()

    def get_all_users(self) -> List:
        session = self._session_cm.session
        models = session.query(self._orm.UserModel).all()
        return [m.to_domain() for m in models]

    def get_total_user_size(self):
        session = self._session_cm.session
        total_size = session.query(func.count(self._orm.UserModel.id)).scalar()
        return total_size or 0

    def create_user(self, username: str, email: str, password_hash: str):
        session = self._session_cm.session
        model = self._orm.UserModel(username=username, email=email, password_hash=password_hash)
        session.add(model)
        session.flush()
        self._session_cm.commit()
        return model.to_domain()

    def get_user_by_email(self, email_clean):
        session = self._session_cm.session
        model = session.query(self._orm.UserModel).filter(func.lower(self._orm.UserModel.email) == email_clean.lower()).first()
        if not model:
            return None
        return model.to_domain()

    def get_user_saved_recipes(self, user):
        session = self._session_cm.session
        # user can be domain User or id
        uid = user.id if hasattr(user, "id") else user
        model = session.query(self._orm.UserModel).filter_by(id=uid).first()
        if not model:
            return []
        return [sr.recipe_id for sr in model.saved_recipes]

    def user_has_saved_recipe(self, recipe, user):
        # normalize recipe to id if a domain Recipe is passed
        recipe_id = recipe.id if hasattr(recipe, "id") else recipe
        saved = self.get_user_saved_recipes(user)
        return recipe_id in saved

    def add_saved_recipe(self, recipe, user):
        session = self._session_cm.session
        uid = user.id if hasattr(user, "id") else user
        model = session.query(self._orm.UserModel).filter_by(id=uid).first()
        if not model:
            raise NoResultFound("User not found")
        # normalize recipe
        recipe_id = recipe.id if hasattr(recipe, "id") else recipe
        # avoid duplicates (but keep domain user in sync)
        existing_ids = [sr.recipe_id for sr in model.saved_recipes]
        if recipe_id in existing_ids:
            # if a domain User was passed, ensure its saved list contains the id
            if hasattr(user, "save_recipe"):
                try:
                    user.save_recipe(recipe_id)
                except Exception:
                    pass
            return
        model.saved_recipes.append(self._orm.UserSavedRecipe(recipe_id=recipe_id))
        self._session_cm.commit()

        # also update domain User object (if provided) so callers that later call
        # repo.update_user(user) won't unintentionally overwrite this new saved recipe
        if hasattr(user, "save_recipe"):
            try:
                user.save_recipe(recipe_id)
            except Exception:
                pass

    def remove_saved_recipe(self, recipe, user):
        session = self._session_cm.session
        uid = user.id if hasattr(user, "id") else user
        model = session.query(self._orm.UserModel).filter_by(id=uid).first()
        if not model:
            return
        recipe_id = recipe.id if hasattr(recipe, "id") else recipe
        # delete the specific association row via ORM so the session is aware
        sr_obj = session.query(self._orm.UserSavedRecipe).filter_by(user_id=uid, recipe_id=recipe_id).first()
        if sr_obj:
            session.delete(sr_obj)
            self._session_cm.commit()
        # keep domain user in sync if provided
        if hasattr(user, "remove_saved_recipe"):
            try:
                user.remove_saved_recipe(recipe_id)
            except Exception:
                pass

    def get_user_recipe_ingredients_by_recipe_name(self, user, recipe_name):
        session = self._session_cm.session
        uid = user.id if hasattr(user, "id") else user
        model = session.query(self._orm.UserModel).filter_by(id=uid).first()
        if not model:
            return []
        # support case-insensitive lookup
        for k, v in (model.recipe_ingredients or {}).items():
            if k.lower() == recipe_name.lower():
                return v
        return []

    def add_user_recipe_ingredient(self, user, recipe_name, ingredient_string):
        session = self._session_cm.session
        uid = user.id if hasattr(user, "id") else user
        model = session.query(self._orm.UserModel).filter_by(id=uid).first()
        if not model:
            raise NoResultFound("User not found")
        ri = model.recipe_ingredients or {}
        # find matching key case-insensitive
        found_key = None
        for k in ri.keys():
            if k.lower() == recipe_name.lower():
                found_key = k
                break
        if not found_key:
            # preserve original case of passed recipe_name
            found_key = recipe_name
            ri[found_key] = []
        # normalize list/tuple entries so qty is always stored as a string
        entry = ingredient_string
        if isinstance(ingredient_string, (list, tuple)):
            qty = ingredient_string[0] if len(ingredient_string) > 0 else ""
            unit = ingredient_string[1] if len(ingredient_string) > 1 else ""
            name = ingredient_string[2] if len(ingredient_string) > 2 else (ingredient_string[-1] if len(ingredient_string) > 0 else "")
            entry = [str(qty) if qty is not None else "", unit if unit is not None else "", name if name is not None else ""]
        if entry not in ri[found_key]:
            ri[found_key].append(entry)
        model.recipe_ingredients = ri
        self._session_cm.commit()

        # keep domain user in sync if a domain User object was passed (use normalized entry)
        if hasattr(user, "add_recipe_ingredient"):
            try:
                user.add_recipe_ingredient(recipe_name, entry)
            except Exception:
                pass

    def remove_user_recipe_ingredient(self, user, recipe_name, ingredient_string):
        session = self._session_cm.session
        uid = user.id if hasattr(user, "id") else user
        model = session.query(self._orm.UserModel).filter_by(id=uid).first()
        if not model:
            return
        ri = model.recipe_ingredients or {}
        # case-insensitive removal
        target = str(ingredient_string).lower()
        for k in list(ri.keys()):
            if k.lower() == recipe_name.lower():
                def _keep(ing):
                    if isinstance(ing, (list, tuple)) and len(ing) > 0:
                        name = str(ing[2]) if len(ing) > 2 else str(ing[-1])
                        return name.lower() != target
                    else:
                        return str(ing).lower() != target

                ri[k] = [ing for ing in ri[k] if _keep(ing)]
                if not ri[k]:
                    del ri[k]
                break
        model.recipe_ingredients = ri
        self._session_cm.commit()

        # keep domain user in sync if provided
        if hasattr(user, "remove_recipe_ingredient"):
            try:
                user.remove_recipe_ingredient(recipe_name, ingredient_string)
            except Exception:
                pass

    def add_multiple_user_recipe_ingredients(self, user, recipe_name, ingredient_strings: List):
        for s in ingredient_strings:
            self.add_user_recipe_ingredient(user, recipe_name, s)

    def remove_multiple_user_recipe_ingredients(self, user, recipe_name, ingredient_strings: List):
        for s in ingredient_strings:
            self.remove_user_recipe_ingredient(user, recipe_name, s)

    def clear_user_recipe_ingredients(self, user, recipe_name):
        session = self._session_cm.session
        uid = user.id if hasattr(user, "id") else user
        model = session.query(self._orm.UserModel).filter_by(id=uid).first()
        if not model:
            return
        ri = model.recipe_ingredients or {}
        # case-insensitive removal
        for k in list(ri.keys()):
            if k.lower() == recipe_name.lower():
                del ri[k]
                break
        model.recipe_ingredients = ri
        self._session_cm.commit()

        # keep domain user in sync if provided
        if hasattr(user, "clear_recipe_ingredients_by_recipe"):
            try:
                user.clear_recipe_ingredients_by_recipe(recipe_name)
            except Exception:
                pass

    def delete_user_recipe_ingredients_per_recipe(self, user, recipe_name):
        # alias to clear
        self.clear_user_recipe_ingredients(user, recipe_name)

    def update_user(self, user):
        session = self._session_cm.session
        # user is domain User
        self._orm.user_from_domain(session, user)
        self._session_cm.commit()

    def add_recipe(self, recipe):
        session = self._session_cm.session
        self._orm.recipe_from_domain(session, recipe)
        self._session_cm.commit()

    def add_multiple_recipes(self, recipes: List):
        for r in recipes:
            self.add_recipe(r)

    def get_recipe_by_name(self, name: str):
        session = self._session_cm.session
        model = (
            session.query(self._orm.RecipeModel)
            .filter(func.lower(self._orm.RecipeModel.name) == name.lower())
            .first()
        )
        if not model:
            return None
        return model.to_domain()

    def get_recipes_by_category(self, category: str) -> List:
        session = self._session_cm.session
        models = (
            session.query(self._orm.RecipeModel)
            .filter(func.lower(self._orm.RecipeModel.category) == category.lower())
            .all()
        )
        return [m.to_domain() for m in models]

    def get_all_recipes(self) -> List:
        session = self._session_cm.session
        models = session.query(self._orm.RecipeModel).all()
        return sorted([m.to_domain() for m in models], key=lambda r: r.name)

    def sort_recipes_by_name(self, name: str):
        session = self._session_cm.session
        models = (
            session.query(self._orm.RecipeModel)
            .filter(func.lower(self._orm.RecipeModel.name).contains(name.lower()))
            .order_by(self._orm.RecipeModel.name)
            .all()
        )
        return [m.to_domain() for m in models]

    def sort_recipes_by_category(self, category: str):
        session = self._session_cm.session
        models = (
            session.query(self._orm.RecipeModel)
            .filter(func.lower(self._orm.RecipeModel.category).contains(category.lower()))
            .order_by(self._orm.RecipeModel.name)
            .all()
        )
        return [m.to_domain() for m in models]
