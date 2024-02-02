from ..models import Category
from ..dtos import CategoryDTO
from app.exceptions.category_exceptions import CategoryNotFoundError, CategoryAlreadyExistsError
from typing import Type


class CategoryService:
    def get_by_id(self, category_id: str):
        category = Category.objects(id=category_id).first()
        if not category:
            return None
        return category

    def get_category_by_title(self, category_title: str, owner_id: str):
        category_exists = Category.objects(owner_id=owner_id, title=category_title.title).first()
        if not category_exists:
            return None
        return category_exists

    def get_by_owner_id(self, category_id: str, owner_id: str):
        category = Category.objects(id=category_id, owner_id=owner_id).first()
        if not category:
            return None
        return category

    def get_all(self):
        all_categories = Category.objects()
        return all_categories

    def create(self, category_dto: CategoryDTO):
        new_category = Category(title=category_dto.title,
                                description=category_dto.description,
                                owner_id=category_dto.owner_id)
        new_category.save()
        return new_category

    def update(self, category_id: str, category_dto: CategoryDTO):
        existing_category = self.get_by_owner_id(category_id=category_id, owner_id=category_dto.owner_id)
        if not existing_category:
            raise CategoryNotFoundError

        existing_category.update(title=category_dto.title,
                                 description=category_dto.description,
                                 owner_id=category_dto.owner_id)
        return existing_category

    def delete_category(self, category_id: str, owner_id: str) -> bool:
        existing_category = self.get_by_owner_id(category_id=category_id, owner_id=owner_id)
        if not existing_category:
            raise CategoryNotFoundError

        existing_category.delete()
        return True
