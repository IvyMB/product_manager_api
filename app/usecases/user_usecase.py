import app.exceptions as app_execptions
from app.dtos import UserDTO, LoginDTO
from app.services import UserService


class UserUseCase:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def get_product_by_id(self, product_id: str):
        return self.user_service.get_by_id(product_id)

    def create_user(self, user_dto: UserDTO):
        user_exists = self.user_service.get_by_email(email=user_dto.email)
        if user_exists:
            raise app_execptions.UserAlreadyExistsError

        result = self.user_service.create(user_dto)
        return result

    def update_user(self, user_id: str, user_dto: UserDTO):
        try:
            result = self.user_service.update_user(user_id=user_id, user_dto=user_dto)
            return result
        except app_execptions.UserNotFoundError:
            raise app_execptions.UserNotFoundError

    def authenticate_user(self, login_dto: LoginDTO):
        email = login_dto.email
        password = login_dto.password

        try:
            json_token_data = self.user_service.authenticate_user(email=email, password=password)
            return json_token_data
        except app_execptions.UserNotFoundError:
            raise app_execptions.UserNotFoundError

        except app_execptions.WrongCredentialsError:
            raise app_execptions.WrongCredentialsError
