from . import bp

from app.models import Demand


@bp.route('/demand', methods=['POST'])
def demand():
    return 'demand placeholder'