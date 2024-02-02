from flask import jsonify, request
from flask.views import MethodView
from ..services import CategoryService
from ..schemas import CategorySchema, DeleteCategorySchema
from ..dtos import CategoryDTO
from app.exceptions.category_exceptions import CategoryNotFoundError, CategoryAlreadyExistsError
from flask_jwt_extended import jwt_required


class CategoryView(MethodView):
    def __init__(self):
        self.category_service = CategoryService()
        self.category_schema = CategorySchema()
        self.delete_schema = DeleteCategorySchema()
        self.many_schema = CategorySchema(many=True)

    def get(self, category_id=None):
        if category_id:
            try:
                category = self.category_service.get_by_id(category_id)
            except CategoryNotFoundError:
                return jsonify({'message': 'Category not found'}), 404

            result = self.category_schema.dump(category)
            return jsonify(result), 200

        all_categories = self.category_service.get_all()
        result = self.many_schema.dump(all_categories)
        return jsonify(result), 200

    @jwt_required()
    def post(self):
        category_data = request.json
        errors = self.category_schema.validate(category_data)
        if errors:
            return jsonify({'message': errors}), 400

        category_dto = CategoryDTO(**category_data)
        try:
            new_category = self.category_service.create(category_dto)
        except CategoryAlreadyExistsError:
            return jsonify({'message': 'Category already exists'}), 404

        result = self.category_schema.dump(new_category)
        return jsonify(result), 201

    @jwt_required()
    def put(self, category_id=None):
        category_data = request.json
        errors = self.category_schema.validate(category_data)
        if errors:
            return jsonify({'message': errors}), 400

        category_dto = CategoryDTO(**category_data)
        try:
            updated_category = self.category_service.update(category_id, category_dto)
        except CategoryNotFoundError:
            return jsonify({'message': 'Category not found'}), 404

        result = self.category_schema.dump(updated_category)
        return jsonify(result), 200

    @jwt_required()
    def delete(self, category_id: str = None):
        if category_id is None:
            return jsonify({'message': 'Category not found'}), 400

        data = request.json
        errors = self.delete_schema.validate(data)
        if errors:
            return jsonify({'message': errors}), 400

        result = self.category_service.category_delete(category_id, data)
        if not result:
            return jsonify({'message': 'Category not found'}), 404

        return jsonify({'message': 'Category deleted successfully'}), 200
