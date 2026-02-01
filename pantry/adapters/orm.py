from typing import List, Dict
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    Table,
    JSON,
    create_engine,
)
from sqlalchemy.orm import relationship, declarative_base, Session
from sqlalchemy.orm import sessionmaker
from pantry.domainmodel.ingredient import Ingredient
from pantry.domainmodel.recipe import Recipe
from pantry.domainmodel.user import User
from pantry.domainmodel.category import Category

Base = declarative_base()

# association table for ingredient <-> category (many-to-many)
ingredient_category = Table(
    "ingredient_category",
    Base.metadata,
    Column("ingredient_id", Integer, ForeignKey("ingredients.id"), primary_key=True),
    Column("category_id", Integer, ForeignKey("categories.id"), primary_key=True),
)


class CategoryModel(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    def to_domain(self) -> Category:
        return Category(self.name)


class IngredientModel(Base):
    __tablename__ = "ingredients"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    unit = Column(String, nullable=True)

    # range and step for UI quantity controls
    range_min = Column(Integer, default=1)
    range_max = Column(Integer, default=100)
    step = Column(Integer, default=1)

    categories = relationship(
        "CategoryModel", secondary=ingredient_category, backref="ingredients"
    )

    def to_domain(self, quantity: float = 0, unit: str = None) -> Ingredient:
        cats = [c.name for c in self.categories] if self.categories else []
        # defensive defaults in case columns are missing or None
        rmin = getattr(self, "range_min", None) or 1
        rmax = getattr(self, "range_max", None) or 100
        stp = getattr(self, "step", None) or 1
        # prefer provided unit; fallback to stored unit or empty string
        use_unit = unit if (unit is not None and unit != "") else (getattr(self, "unit", None) or "")
        return Ingredient(self.name, quantity, use_unit, categories=cats, range_min=rmin, range_max=rmax, step=stp)


# --- New: recipe-specific ingredient model (decoupled from inventory ingredients) ---
class RecipeIngredientModel(Base):
    __tablename__ = "recipe_ingredients"
    id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    name = Column(String, nullable=False)
    quantity = Column(Float, nullable=True)
    unit = Column(String, nullable=True)
    position = Column(Integer, nullable=True)

    recipe = relationship("RecipeModel", back_populates="recipe_ingredients")


class RecipeModel(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    methods = Column(JSON, default=[])
    prep_time_mins = Column(Integer, default=0)
    cook_time_mins = Column(Integer, default=0)
    total_time_mins = Column(Integer, default=0)
    difficulty = Column(String, nullable=True)
    category = Column(String, nullable=True)
    cuisine = Column(String, nullable=True)
    tags = Column(JSON, default=[])
    notes = Column(String, nullable=True)
    image_url = Column(String, nullable=True)

    # now use recipe-specific ingredient rows
    recipe_ingredients = relationship(
        "RecipeIngredientModel", back_populates="recipe", cascade="all, delete-orphan"
    )

    def to_domain(self) -> Recipe:
        ingredients = []
        # convert each recipe ingredient to the domain triple (name, qty, unit)
        for ri in sorted(self.recipe_ingredients, key=lambda a: (a.position or 0)):
            # preserve missing quantities as empty string (do not coerce None -> 0)
            if ri.quantity is None:
                qty_str = ""
            else:
                # format numeric values: prefer integer representation when possible
                try:
                    qf = float(ri.quantity)
                    if qf.is_integer():
                        qty_str = str(int(qf))
                    else:
                        qty_str = str(qf)
                except Exception:
                    qty_str = str(ri.quantity)

            unit = ri.unit or ""
            # return (qty, unit, name) to match datareader/template expectations
            ingredients.append((qty_str, unit, ri.name))
        return Recipe(
            id=self.id,
            name=self.name,
            description=self.description or "",
            ingredients=ingredients,
            methods=self.methods or [],
            prep_time_mins=self.prep_time_mins or 0,
            cook_time_mins=self.cook_time_mins or 0,
            total_time_mins=self.total_time_mins or 0,
            difficulty=self.difficulty or "",
            category=self.category or "",
            cuisine=self.cuisine or "",
            tags=self.tags or [],
            notes=self.notes or "",
            image_url=self.image_url or "",
        )


class UserGroceryAssoc(Base):
    __tablename__ = "user_grocery"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"))
    quantity = Column(Float, nullable=False)

    ingredient = relationship("IngredientModel")


class UserSavedRecipe(Base):
    __tablename__ = "user_saved_recipes"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    recipe_id = Column(Integer, ForeignKey("recipes.id"))


class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=False)
    password_hash = Column(String, nullable=True)
    # store mapping recipe_name -> list[str] to match domain model
    recipe_ingredients = Column(JSON, default={})

    grocery_assocs = relationship(
        "UserGroceryAssoc", cascade="all, delete-orphan", backref="user"
    )
    saved_recipes = relationship(
        "UserSavedRecipe", cascade="all, delete-orphan", backref="user"
    )

    def to_domain(self) -> User:
        u = User(self.id, self.username, self.email, self.password_hash)
        # grocery list -> produce Ingredient domain objects with stored quantity
        for assoc in self.grocery_assocs:
            ingr = assoc.ingredient.to_domain(quantity=assoc.quantity, unit="")
            u.add_grocery(ingr, assoc.quantity)
        # saved recipes ids
        for sr in self.saved_recipes:
            u.save_recipe(sr.recipe_id)
        # recipe_ingredients JSON expected to be dict[str, list[str]]
        if isinstance(self.recipe_ingredients, dict):
            u.clear_all_recipe_ingredients()
            for k, v in self.recipe_ingredients.items():
                u.add_multiple_recipe_ingredients(k, v)
        return u


# Helper convenience functions

def ensure_category(session: Session, name: str) -> CategoryModel:
    name = name.strip()
    obj = session.query(CategoryModel).filter_by(name=name).first()
    if obj:
        return obj
    obj = CategoryModel(name=name)
    session.add(obj)
    session.flush()
    return obj


def ensure_ingredient(session: Session, name: str) -> IngredientModel:
    name = name.strip()
    obj = session.query(IngredientModel).filter_by(name=name).first()
    if obj:
        return obj
    obj = IngredientModel(name=name)
    session.add(obj)
    session.flush()
    return obj


def recipe_from_domain(session: Session, domain: Recipe) -> RecipeModel:
    rm = session.query(RecipeModel).filter_by(id=domain.id).first()
    if not rm:
        rm = RecipeModel(id=domain.id)
        session.add(rm)
    rm.name = domain.name
    rm.description = domain.description
    rm.methods = domain.methods
    rm.prep_time_mins = domain.prep_time_mins
    rm.cook_time_mins = domain.cook_time_mins
    rm.total_time_mins = domain.total_time_mins
    rm.difficulty = domain.difficulty
    rm.category = domain.category
    rm.cuisine = domain.cuisine
    rm.tags = domain.tags
    rm.notes = domain.notes
    rm.image_url = domain.image_url

    # rebuild recipe-specific ingredient rows (do NOT touch global inventory ingredients)
    rm.recipe_ingredients.clear()

    def _extract_number_token(s: str):
        import re
        if s is None:
            return None
        s = str(s)
        # match an integer or decimal (first occurrence), also handle ranges like 900-1000 by grabbing first number
        m = re.search(r"\d+(?:\.\d+)?", s)
        if not m:
            return None
        try:
            return float(m.group(0))
        except Exception:
            return None

    for pos, entry in enumerate(domain.ingredients):
        name = ""
        qty = None
        unit = ""

        if isinstance(entry, (tuple, list)):
            # normalize parts, keep empty strings as placeholders
            parts = [p.strip() for p in entry if p is not None]
            parts = [p for p in parts if p != ""]

            # try qty in first part
            if len(parts) >= 1 and _extract_number_token(parts[0]) is not None:
                qty = _extract_number_token(parts[0])
                unit = parts[1] if len(parts) > 1 else ""
                name = " ".join(parts[2:]) if len(parts) > 2 else ""
            # try qty in second part (name, qty, unit)
            elif len(parts) >= 2 and _extract_number_token(parts[1]) is not None:
                name = parts[0]
                qty = _extract_number_token(parts[1])
                unit = parts[2] if len(parts) > 2 else ""
                if len(parts) > 3:
                    # append any trailing tokens to name
                    name = name + " " + " ".join(parts[3:])
            else:
                # fallback: no numeric quantity found
                if len(parts) == 1:
                    name = parts[0]
                elif len(parts) == 2:
                    name = parts[1]
                    unit = parts[0]
                else:
                    name = " ".join(parts[2:]) if len(parts) > 2 else parts[-1]
                    unit = parts[1] if len(parts) > 1 else ""
        elif isinstance(entry, Ingredient):
            name, qty, unit = entry.name, entry.quantity, entry.unit
        else:
            # unexpected type; skip
            continue

        name = (name or "").strip()
        unit = (unit or "").strip()

        # if name is empty but parts had something, try to salvage last token
        if not name and isinstance(entry, (tuple, list)) and len(entry) > 0:
            name = str(entry[-1]).strip()

        # ensure numeric qty or None
        if isinstance(qty, str):
            qty = _extract_number_token(qty)

        qty_val = float(qty) if (qty is not None) else None

        # skip associations without a sensible ingredient name
        if not name:
            continue

        # create a recipe-specific ingredient row (decoupled from inventory IngredientModel)
        rim = RecipeIngredientModel(name=name, quantity=qty_val, unit=unit or "", position=pos)
        rm.recipe_ingredients.append(rim)
    session.flush()
    return rm


def user_from_domain(session: Session, domain: User) -> UserModel:
    um = session.query(UserModel).filter_by(id=domain.id).first()
    if not um:
        um = UserModel(id=domain.id)
        session.add(um)
    um.username = domain.username
    um.email = domain.email
    um.password_hash = domain.password_hash
    # recipe_ingredients stored as a dict mapping recipe_name -> list[str]
    um.recipe_ingredients = domain.recipe_ingredients if isinstance(domain.recipe_ingredients, dict) else {}
    # rebuild grocery associations
    um.grocery_assocs.clear()
    for ing in domain.grocery_list:
        ingr_model = ensure_ingredient(session, ing.name)
        assoc = UserGroceryAssoc(ingredient=ingr_model, quantity=ing.quantity or 0)
        um.grocery_assocs.append(assoc)
    # saved recipes
    um.saved_recipes.clear()
    for rid in domain.saved_recipes:
        um.saved_recipes.append(UserSavedRecipe(recipe_id=rid))
    session.flush()
