import app.exceptions as app_execptions
from app.dtos import CategoryDTO
from app.services import CategoryService


class CategoryUseCase:
    def __init__(self, category_service: CategoryService):
        self.category_service = category_service

    def get_all_categories(self):
        return self.category_service.get_all()

    def get_category_by_id(self, category_id: str):
        return self.category_service.get_by_id(category_id)

    def create_category(self, category_dto: CategoryDTO):
        category_exists = self.category_service.get_category_by_title(category_title=category_dto.title,
                                                                      owner_id=category_dto.owner_id)
        if category_exists:
            raise app_execptions.CategoryAlreadyExistsError
        result = self.category_service.create(category_dto)
        return result

    def update_category(self, category_id: str, category_dto: CategoryDTO):
        try:
            result = self.category_service.update(category_id=category_id, category_dto=category_dto)
            return result
        except app_execptions.CategoryNotFoundError:
            raise app_execptions.CategoryNotFoundError

    def delete_category(self, category_id: str, owner_data: dict[str]):
        owner_id = owner_data['owner_id']
        try:
            self.category_service.delete_category(category_id=category_id, owner_id=owner_id)
        except app_execptions.CategoryNotFoundError:
            raise app_execptions.CategoryNotFoundError
