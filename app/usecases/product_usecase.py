import app.exceptions as app_execptions
from app.dtos import ProductDTO
from app.services import ProductService, CategoryService


class ProductUseCase:
    def __init__(self, product_service: ProductService, category_service: CategoryService):
        self.product_service = product_service
        self.category_service = category_service

    def get_all_products(self):
        return self.product_service.get_all()

    def get_product_by_id(self, product_id: str):
        return self.product_service.get_by_id(product_id)

    def create_product(self, product_dto: ProductDTO):
        product_exists = self.product_service.check_product_exists_for_owner(title=product_dto.title,
                                                                             owner_id=product_dto.owner_id)
        if product_exists:
            raise app_execptions.ProductAlreadyExistsError

        category_exists = self.category_service.get_by_id(category_id=product_dto.category)
        if not category_exists:
            raise app_execptions.CategoryNotFoundError

        result = self.product_service.create(product_dto)
        return result

    def update_product(self, product_id: str, product_dto: ProductDTO):
        try:
            result = self.product_service.update_product(product_id=product_id, product_dto=product_dto)
            return result
        except app_execptions.ProductNotFoundError:
            raise app_execptions.ProductNotFoundError

    def delete_product(self, product_id: str, owner_data: dict[str]):
        owner_id = owner_data['owner_id']
        try:
            self.product_service.delete_product(product_id=product_id, owner_id=owner_id)
        except app_execptions.ProductNotFoundError:
            raise app_execptions.ProductNotFoundError
