from flask import Blueprint
from ..views import UserView

user_blueprint = Blueprint('user', __name__)
user_view = UserView.as_view('user_view')

user_blueprint.add_url_rule('/api/users', view_func=user_view, methods=['POST'])
user_blueprint.add_url_rule('/api/users/<string:user_id>', view_func=user_view, methods=['PUT'])
