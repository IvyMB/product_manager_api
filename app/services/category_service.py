from ..models import Category
from ..dtos import CategoryDTO


class CategoryService:

    def get_by_id(self, category_id: str):
        category = Category.objects(id=category_id).first()
        return category

    def get_all(self):
        all_categories = Category.objects()
        return all_categories

    def create(self, category_dto: CategoryDTO):
        category = Category.objects(owner_id=category_dto.owner_id, title=category_dto.title).first()
        if not category:
            new_category = Category(title=category_dto.title,
                                    description=category_dto.description,
                                    owner_id=category_dto.owner_id)
            new_category.save()
            return new_category
        return None

    def update(self, category_id: str, category_dto: CategoryDTO):
        existing_category = self.get_by_id(category_id)
        if existing_category:
            existing_category.modify(title=category_dto.title,
                                     description=category_dto.description,
                                     owner_id=category_dto.owner_id)
            return existing_category
        return None

    def category_delete(self, category_id: str) -> None:
        existing_category = self.get_by_id(category_id)
        if existing_category:
            existing_category.category_delete()
