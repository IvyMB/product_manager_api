from flask_bcrypt import check_password_hash, generate_password_hash
from datetime import timedelta
from flask_jwt_extended import create_access_token
from ..models import User
from ..dtos import UserDTO, LoginDTO
from app.exceptions import UserAlreadyExistsError, UserNotFoundError, WrongCredentialsError


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

    def authenticate_user(self, email: str, password: str):
        user = self.get_by_email(email)
        if not user:
            raise UserNotFoundError

        if not self.verify_password(user.password, password):
            raise WrongCredentialsError

        token = self.generate_token(user.id)
        return {'user_id': str(user.id), 'username': str(user.username), 'token': token}

    def create(self, user_dto: UserDTO):
        hashed_password = self.create_hashed_password(user_dto.password)
        new_user = User(username=user_dto.username,
                        password=hashed_password,
                        email=user_dto.email,
                        roles=user_dto.roles,
                        store_id=user_dto.store_id)
        new_user.save()
        return new_user

    def update_user(self, user_id: str, user_dto: UserDTO):
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
