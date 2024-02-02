from ..models import User
from ..dtos import UserDTO, LoginDTO
from app.exceptions import UserAlreadyExistsError, UserNotFoundError, WrongCredentialsError
from flask_bcrypt import check_password_hash, generate_password_hash
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token


class UserService:
    def get_by_id(self, user_id: str):
        user = User.objects(id=user_id).first()
        if not user:
            raise UserNotFoundError
        return user

    def get_by_email(self, email: str):
        user = User.objects(email=email).first()
        if not user:
            raise UserNotFoundError
        return user

    def create_hashed_password(self, password: str):
        hashed_password = generate_password_hash(password.encode('utf-8'))
        return hashed_password

    def verify_password(self, hashed_password: str, password: str):
        return check_password_hash(hashed_password, password)

    def generate_token(self, user_id: str):
        token = create_access_token(identity=str(user_id), expires_delta=timedelta(days=1))
        return token

    def authenticate_user(self, login_dto: LoginDTO):
        email_data = login_dto.email
        password_data = login_dto.password
        user = self.get_by_email(email_data)
        if not user:
            raise UserNotFoundError

        if not self.verify_password(user.password, password_data):
            raise WrongCredentialsError

        token = self.generate_token(user.id)
        return {'user_id': str(user.id), 'username': str(user.username), 'token': token}

    def create(self, user_dto: UserDTO):
        user_exists = User.objects(email=user_dto.email).first()
        if user_exists:
            raise UserAlreadyExistsError("User already exists.")

        hashed_password = self.create_hashed_password(user_dto.password)
        new_user = User(username=user_dto.username,
                        password=hashed_password,
                        email=user_dto.email,
                        roles=user_dto.roles,
                        store_id=user_dto.store_id)
        new_user.save()
        return new_user

    def user_update(self, user_id: str, user_dto: UserDTO):
        try:
            existing_user = self.get_by_id(user_id)
        except UserNotFoundError:
            return None

        update_data = {
            'username': user_dto.username,
            'password': user_dto.password,
            'email': user_dto.email,
            'active': user_dto.active,
            'store_id': user_dto.store_id,
        }

        update_data = {key: value for key, value in update_data.items() if value is not None and value != ''}
        existing_user.update(**update_data)
        return existing_user
