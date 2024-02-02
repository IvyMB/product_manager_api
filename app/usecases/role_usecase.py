import app.exceptions as app_execptions
from app.dtos import RoleDTO
from app.services import RoleService


class RoleUseCase:
    def __init__(self, role_service: RoleService):
        self.role_service = role_service

    def get_all_roles(self):
        return self.role_service.get_all()

    def create_role(self, role_dto: RoleDTO):
        role_exists = self.role_service.get_by_name(name=role_dto.name)
        if role_exists:
            raise app_execptions.RoleAlreadyExistsError

        result = self.role_service.create(role_dto)
        return result
