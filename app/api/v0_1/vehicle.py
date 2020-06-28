from . import bp

from app.models import Vehicle


@bp.route('/vehicle', methods=['POST'])
def vehicle():
    return 'vehicle placeholder'