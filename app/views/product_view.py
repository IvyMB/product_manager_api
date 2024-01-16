from flask import jsonify, request
from flask.views import MethodView
from ..schemas import ProductSchema
from ..services import ProductService, CategoryService
from flask import abort
from ..dtos import ProductDTO
from app.exceptions.category_exceptions import CategoryNotFoundError
from app.exceptions import ProductAlreadyExistsError, ProductNotFoundError


class ProductView(MethodView):
    def __init__(self):
        self.product_service = ProductService()
        self.category_service = CategoryService()
        self.product_schema = ProductSchema()
        self.product_many_schema = ProductSchema(many=True)

    def get(self, product_id=None):
        if product_id:
            try:
                product = self.product_service.get_by_id(product_id)
            except ProductNotFoundError:
                return jsonify({'errors': 'Product not found'}), 404

            result = self.product_schema.dump(product)
            print(result)
            return jsonify(result), 200

        all_products = self.product_service.get_all()
        result = self.product_many_schema.dump(all_products)
        return jsonify(result), 200

    def post(self):
        product_data = request.json
        errors = self.product_schema.validate(product_data)
        if errors:
            return jsonify({'errors': errors}), 400

        product_dto = ProductDTO(**product_data)
        try:
            new_product = self.product_service.create(product_dto, self.category_service)
        except CategoryNotFoundError:
            return jsonify({'errors': 'Category not found'}), 404
        except ProductAlreadyExistsError:
            return jsonify({'errors': 'Product already exists'}), 400

        result = self.product_schema.dump(new_product)
        return jsonify(result), 201

    def put(self, product_id=None):
        if product_id is None:
            return jsonify({'message': 'Product not found'}), 404

        product_data = request.json
        errors = self.product_schema.validate(product_data)
        if errors:
            return jsonify({'errors': errors}), 400

        update_product_dto = ProductDTO(**product_data)
        try:
            updated_product = self.product_service.product_update(product_id, update_product_dto)
        except ProductNotFoundError:
            return jsonify({'errors': 'Product not found'}), 404

        result = self.product_schema.dump(updated_product)
        return jsonify(result), 200

    def delete(self, product_id=None):
        if product_id is None:
            return jsonify({'message': 'Product not found'}), 404

        try:
            self.product_service.product_delete(product_id)
        except ProductNotFoundError:
            return jsonify({'errors': 'Product not found'}), 404
        return jsonify({'message': 'Product deleted successfully'}), 200
