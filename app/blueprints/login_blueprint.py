from flask import Blueprint
from ..views import LoginView

login_blueprint = Blueprint('login', __name__)
login_view = LoginView.as_view('login_view')

login_blueprint.add_url_rule('/api/login', view_func=login_view, methods=['POST'])
