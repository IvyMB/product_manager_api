from flask import jsonify, request
from flask.views import MethodView
from ..schemas import RoleSchema
from ..services import RoleService
from ..dtos import RoleDTO
from app.exceptions.role_exceptions import RoleNotFoundError, RoleAlreadyExistsError
from flask_jwt_extended import jwt_required


class RoleView(MethodView):
    def __init__(self):
        self.role_service = RoleService()
        self.role_schema = RoleSchema()
        self.role_many_schema = RoleSchema(many=True)

    def get(self, role_name: str = None):
        if role_name:
            try:
                role = self.role_service.get_by_name(role_name)
            except RoleNotFoundError:
                return jsonify({'message': 'Role not found'}), 404

            result = self.role_schema.dump(role)
            return jsonify(result), 200

        all_roles = self.role_service.get_all()
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
            new_role = self.role_service.create(role_dto)
        except RoleNotFoundError:
            return jsonify({'message': 'Role not found'}), 404
        except RoleAlreadyExistsError:
            return jsonify({'message': 'Role already exists'}), 400

        result = self.role_schema.dump(new_role)
        return jsonify(result), 201
