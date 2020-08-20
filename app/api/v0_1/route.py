from . import bp

from app.models import Route


@bp.route("/solution", methods=["POST"])
def solution():
    return "solution placeholder"
