from flask import jsonify, request
from flask.views import MethodView
from ..services import UserService
from ..schemas import UserCreateSchema, UserUpdateSchema
from ..dtos import UserDTO
from ..exceptions import UserAlreadyExistsError, UserNotFoundError
from flask_jwt_extended import jwt_required


class UserView(MethodView):
    def __init__(self):
        self.user_service = UserService()
        self.create_schema = UserCreateSchema()
        self.update_schema = UserUpdateSchema()

    def post(self):
        user_data = request.json
        errors = self.create_schema.validate(user_data)
        if errors:
            return jsonify({'errors': errors}), 400

        user_dto = UserDTO(**user_data)
        try:
            new_user = self.user_service.create(user_dto)
        except UserAlreadyExistsError:
            return jsonify({'message': 'User already exists'}), 404

        result = self.create_schema.dump(new_user)
        return jsonify(result), 201

    @jwt_required()
    def put(self, user_id=None):
        if user_id is None:
            return jsonify({'message': 'Product not found'}), 404

        user_data = request.json
        errors = self.update_schema.validate(user_data)
        if errors:
            return jsonify({'message': errors}), 400

        user_dto = UserDTO(**user_data)
        try:
            updated_user = self.user_service.user_update(user_id, user_dto)
        except UserNotFoundError:
            return jsonify({'message': 'Category not found'}), 404

        result = self.update_schema.dump(updated_user)
        return jsonify(result), 200
