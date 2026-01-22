from flask import Blueprint, render_template, redirect, url_for, session, jsonify
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from password_validator import PasswordValidator

from pantry.adapters import repository
from pantry.blueprints.authentication import services
from pantry.utilities.auth import is_logged_in

authentication_blueprint = Blueprint("authentication_bp", __name__, url_prefix="/auth")


@authentication_blueprint.route("/login", methods=["GET", "POST"])
def login():
    repo = repository.repo_instance
    form = LoginForm()
    username_not_recognized = None
    password_does_not_match = None

    if form.validate_on_submit():
        try:
            user = services.get_user(form.username.data, repo)

            services.authenticate_user(user["username"], form.password.data, repo)

            session.clear()

            session["username"] = user["username"]
            return redirect(url_for("home_bp.home"))

        except services.UnknownUserException:
            username_not_recognized = "Username not recognized"

        except services.AuthenticationException:
            password_does_not_match = "Password does not match"

    return render_template(
        "pages/auth/login.html",
        title="Login",
        form=form,
        username_not_recognized=username_not_recognized,
        password_does_not_match=password_does_not_match,
        handler_url=url_for("authentication_bp.login"),
    )


@authentication_blueprint.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home_bp.home"))


def login_required(view):
    from functools import wraps

    @wraps(view)
    def wrapped_view(**kwargs):
        if not is_logged_in():
            return redirect(url_for("authentication_bp.login"))
        return view(**kwargs)

    return wrapped_view


@authentication_blueprint.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    username_error_message = None
    email_error_message = None

    if form.validate_on_submit():
        if len(form.username.data.strip()) > 20:
            username_error_message = "Your username is too long"
            return render_template(
                "pages/auth/register.html",
                title="Register",
                form=form,
                username_error_message=username_error_message,
                handler_url=url_for("authentication_bp.register"),
            )

        else:
            password_hash = generate_password_hash(form.password.data)
            try:
                services.add_user(
                    form.username.data,
                    form.email.data,
                    password_hash,
                    repository.repo_instance,
                )
                return redirect(url_for("authentication_bp.login"))
            except services.NameNotUniqueException:
                username_error_message = (
                    "Username already exists - please choose another"
                )

            except services.EmailNotUniqueException:
                email_error_message = "Email already registered - please use another"
    return render_template(
        "pages/auth/register.html",
        title="Register",
        form=form,
        username_error_message=username_error_message,
        email_error_message=email_error_message,
        handler_url=url_for("authentication_bp.register"),
    )


class PasswordValid:
    def __init__(self, message=None):
        if not message:
            message = (
                "Your password must be at least 8 characters, and contain an upper case letter,\
            a lower case letter and a digit"
            )
        self.message = message

    def __call__(self, form, field):
        schema = PasswordValidator()
        schema.min(8).has().uppercase().has().lowercase().has().digits()
        if not schema.validate(field.data):
            raise ValidationError(self.message)


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username",
        [
            DataRequired(message="Your user name is required"),
            Length(min=3, message="Your user name is too short"),
        ],
    )
    email = StringField(
        "Email",
        [
            DataRequired(message="Your email is required"),
            Length(min=9, message="Your email is too short"),
        ],
    )
    password = PasswordField(
        "Password", [DataRequired(message="Your password is required"), PasswordValid()]
    )
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    username = StringField("Username", [DataRequired()])
    password = PasswordField("Password", [DataRequired()])
    submit = SubmitField("Login")
