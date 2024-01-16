from flask import Blueprint
from ..views import ProductView

product_blueprint = Blueprint('product', __name__)
product_view = ProductView.as_view('product_view')

product_blueprint.add_url_rule('/api/products', view_func=product_view, methods=['GET', 'POST'])
product_blueprint.add_url_rule('/api/products/<product_id>', view_func=product_view, methods=['GET', 'PUT', 'DELETE'])