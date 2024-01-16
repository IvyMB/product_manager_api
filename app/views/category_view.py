from flask import jsonify, request
from flask.views import MethodView
from ..services import CategoryService
from ..schemas import CategorySchema
from ..dtos import CategoryDTO
from app.exceptions.category_exceptions import CategoryNotFoundError, CategoryAlreadyExistsError


class CategoryView(MethodView):
    def __init__(self):
        self.category_service = CategoryService()
        self.schema = CategorySchema()
        self.many_schema = CategorySchema(many=True)

    def get(self, category_id=None):
        if category_id:
            try:
                category = self.category_service.get_by_id(category_id)
            except CategoryNotFoundError:
                return jsonify({'errors': 'Category not found'}), 404

            result = self.schema.dump(category)
            return jsonify(result), 200

        all_categories = self.category_service.get_all()
        result = self.many_schema.dump(all_categories)
        return jsonify(result), 200

    def post(self):
        category_data = request.json
        errors = self.schema.validate(category_data)
        if errors:
            return jsonify({'errors': errors}), 400

        category_dto = CategoryDTO(**category_data)
        try:
            new_category = self.category_service.create(category_dto)
        except CategoryAlreadyExistsError:
            return jsonify({'message': 'Category already exists'}), 404

        result = self.schema.dump(new_category)
        return jsonify(result), 201

    def put(self, category_id=None):
        category_data = request.json
        errors = self.schema.validate(category_data)
        if errors:
            return jsonify({'errors': errors}), 400

        category_dto = CategoryDTO(**category_data)
        try:
            updated_category = self.category_service.update(category_id, category_dto)
        except CategoryNotFoundError:
            return jsonify({'errors': 'Category not found'}), 404
        
        result = self.schema.dump(updated_category)
        return jsonify(result), 200

    def delete(self, category_id=None):
        if category_id is None:
            return jsonify({'message': 'Product not found'}), 400
        
        self.category_service.category_delete(category_id)
        return jsonify({'message': 'Product deleted successfully'}), 200
