from flask import jsonify, request
from flask.views import MethodView
from ..schemas import ProductSchema, DeleteProductSchema
from ..usecases import ProductUseCase
from ..services import ProductService, CategoryService
from ..dtos import ProductDTO
import app.exceptions as app_exceptions
from flask_jwt_extended import jwt_required, get_jwt_identity


class ProductView(MethodView):
    def __init__(self):
        self.product_service = ProductService()
        self.category_service = CategoryService()
        self.product_usecase = ProductUseCase(self.product_service, self.category_service)
        self.product_schema = ProductSchema()
        self.delete_product_schema = DeleteProductSchema()
        self.product_many_schema = ProductSchema(many=True)

    def get(self, product_id=None):
        if product_id:
            try:
                product = self.product_usecase.get_product_by_id(product_id)
            except app_exceptions.ProductNotFoundError:
                return jsonify({'message': 'Product not found'}), 404

            result = self.product_schema.dump(product)
            print(result)
            return jsonify(result), 200

        all_products = self.product_usecase.get_all_products()
        result = self.product_many_schema.dump(all_products)
        return jsonify(result), 200

    @jwt_required()
    def post(self):
        product_data = request.json
        errors = self.product_schema.validate(product_data)
        if errors:
            return jsonify({'message': errors}), 400

        product_dto = ProductDTO(**product_data)
        try:
            new_product = self.product_usecase.create_product(product_dto)
        except app_exceptions.CategoryNotFoundError:
            return jsonify({'message': 'Category not found'}), 404
        except app_exceptions.ProductAlreadyExistsError:
            return jsonify({'message': 'Product already exists'}), 400

        result = self.product_schema.dump(new_product)
        return jsonify(result), 201

    @jwt_required()
    def put(self, product_id=None):
        if product_id is None:
            return jsonify({'message': 'Product not found'}), 404

        product_data = request.json
        errors = self.product_schema.validate(product_data)
        if errors:
            return jsonify({'message': errors}), 400

        update_product_dto = ProductDTO(**product_data)
        try:
            updated_product = self.product_service.update_product(product_id, update_product_dto)
        except app_exceptions.ProductNotFoundError:
            return jsonify({'message': 'Product not found'}), 404

        result = self.product_schema.dump(updated_product)
        return jsonify(result), 200

    @jwt_required()
    def delete(self, product_id=None):
        if product_id is None:
            return jsonify({'message': 'Product not found'}), 404
        data = request.json
        errors = self.delete_product_schema.validate(data)
        if errors:
            return jsonify({'message': errors}), 400

        try:
            result = self.product_service.delete_product(product_id, data)
        except app_exceptions.ProductNotFoundError:
            return jsonify({'message': 'Product not found'}), 404

        return jsonify({'message': 'Product deleted successfully'}), 200
