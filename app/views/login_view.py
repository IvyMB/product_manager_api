from flask import jsonify, request
from flask.views import MethodView
from ..usecases import UserUseCase
from ..schemas import LoginSchema
from ..dtos import LoginDTO
from ..exceptions import WrongCredentialsError, UserNotFoundError


class LoginView(MethodView):
    def __init__(self):
        self.user_usecase = UserUseCase(self.user_service)
        self.login_schema = LoginSchema()

    def post(self):
        login_data = request.json
        errors = self.login_schema.validate(login_data)
        if errors:
            return jsonify({'message': errors}), 400

        login_dto = LoginDTO(**login_data)
        try:
            result = self.user_usecase.authenticate_user(login_dto)
        except UserNotFoundError:
            return jsonify({'message': "Doesn't exist an user with this email"}), 404
        except WrongCredentialsError:
            return jsonify({'message': "Wrong credentials"}), 401

        return jsonify(result), 200
