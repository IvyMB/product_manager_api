from flask import Blueprint
from ..views import RoleView

role_blueprint = Blueprint('role', __name__)
role_view = RoleView.as_view('role_view')

role_blueprint.add_url_rule('/api/role', view_func=role_view, methods=['POST', 'GET'])
