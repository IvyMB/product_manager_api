from flask import Blueprint
from ..views import CategoryView

category_blueprint = Blueprint('category', __name__)
category_view = CategoryView.as_view('category_view')

category_blueprint.add_url_rule('/api/categories', view_func=category_view, methods=['GET', 'POST'])
category_blueprint.add_url_rule('/api/categories/<category_id>', view_func=category_view, methods=['GET', 'PUT', 'DELETE'])