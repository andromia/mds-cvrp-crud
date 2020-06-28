from . import bp

from app.models import Origin


@bp.route('/origin', methods=['POST'])
def origin():
    return 'origin placeholder'