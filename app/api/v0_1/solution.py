from . import bp

from app.models import Solution


@bp.route("/solution", methods=["POST"])
def solution():
    return "solution placeholder"
