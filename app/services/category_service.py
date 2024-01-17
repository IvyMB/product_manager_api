from ..models import Category
from ..dtos import CategoryDTO
from app.exceptions.category_exceptions import CategoryNotFoundError, CategoryAlreadyExistsError


class CategoryService:

    def get_by_id(self, category_id: str):
        category = Category.objects(id=category_id).first()
        if not category:
            raise CategoryNotFoundError
        return category

    def get_all(self):
        all_categories = Category.objects()
        return all_categories

    def create(self, category_dto: CategoryDTO):
        category = Category.objects(owner_id=category_dto.owner_id, title=category_dto.title).first()
        if category:
            raise CategoryAlreadyExistsError
        new_category = Category(title=category_dto.title,
                                description=category_dto.description,
                                owner_id=category_dto.owner_id)
        new_category.save()
        return new_category

    def update(self, category_id: str, category_dto: CategoryDTO):
        try:
            existing_category = self.get_by_id(category_id)
        except CategoryNotFoundError:
            return None
        existing_category.update(title=category_dto.title,
                                 description=category_dto.description,
                                 owner_id=category_dto.owner_id)
        return existing_category

    def category_delete(self, category_id: str) -> bool:
        try:
            existing_category = self.get_by_id(category_id)
        except CategoryNotFoundError:
            return False

        existing_category.delete()
        return True
