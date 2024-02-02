from flask import jsonify, request
from flask.views import MethodView
from ..schemas import RoleSchema
from ..services import RoleService
from ..usecases import RoleUseCase
from ..dtos import RoleDTO
from app.exceptions.role_exceptions import RoleNotFoundError, RoleAlreadyExistsError
from flask_jwt_extended import jwt_required


class RoleView(MethodView):
    def __init__(self):
        self.role_service = RoleService()
        self.role_usecase = RoleUseCase(self.role_service)
        self.role_schema = RoleSchema()
        self.role_many_schema = RoleSchema(many=True)

    def get(self):
        all_roles = self.role_usecase.get_all_roles()
        result = self.role_many_schema.dump(all_roles)
        return jsonify(result), 200

    @jwt_required()
    def post(self):
        role_data = request.json
        errors = self.role_schema.validate(role_data)
        if errors:
            return jsonify({'message': errors}), 400

        role_dto = RoleDTO(**role_data)
        try:
            new_role = self.role_usecase.create_role(role_dto)
        except RoleNotFoundError:
            return jsonify({'message': 'Role not found'}), 404
        except RoleAlreadyExistsError:
            return jsonify({'message': 'Role already exists'}), 400

        result = self.role_schema.dump(new_role)
        return jsonify(result), 201
