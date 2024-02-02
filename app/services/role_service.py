from ..models import Role
from ..dtos import RoleDTO
from app.exceptions.role_exceptions import RoleAlreadyExistsError, RoleNotFoundError
import logging


class RoleService:
    def get_by_name(self, name: str):
        role = Role.objects(name=name).first()
        if not role:
            raise RoleNotFoundError
        return role

    def get_all(self):
        all_roles = Role.objects()
        return all_roles

    def create(self, role_dto: RoleDTO,):
        new_role = Role(name=role_dto.name)
        new_role.save()
        return new_role

    def role_delete(self, role_name: str) -> None:
        try:
            existing_product = self.get_by_name(role_name)
        except RoleNotFoundError:
            return None

        existing_product.delete()
