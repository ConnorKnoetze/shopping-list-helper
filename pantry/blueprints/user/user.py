from flask import Blueprint, session

from pantry.utilities.auth import _repo
from pantry.blueprints.authentication.authentication import login_required

user_bp = Blueprint("user", __name__)

@user_bp.route("/user/<string:username>")
@login_required
def user_profile(username: str):
    """
    Renders the user profile page for the specified username.
    :param username:
    :return:
    Rendered user profile template.
    """
    from flask import render_template

    if username != session['username']:
        return render_template("errors/403.html"), 403

    repo = _repo()
    user = repo.get_user_by_username(username)

    if not user:
        return render_template("errors/404.html"), 404

    return render_template(
        "pages/user/user.html",
        user=user,
        username_shorthand= user.username[0].upper(),
    )