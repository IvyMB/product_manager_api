from ..models import Product
from ..dtos import ProductDTO
from .category_service import CategoryService
from app.exceptions.category_exceptions import CategoryNotFoundError
from app.exceptions import ProductAlreadyExistsError, ProductNotFoundError


class ProductService:
    def get_by_id(self, product_id: str):
        product = Product.objects(id=product_id).first()
        if not product:
            raise ProductNotFoundError
        return product

    def get_all(self):
        all_products = Product.objects()
        return all_products

    def create(self, product_dto: ProductDTO, category_service: CategoryService):
        product_exists = Product.objects(title=product_dto.title, owner_id=product_dto.owner_id).first()
        if product_exists:
            raise ProductAlreadyExistsError("Product already exists.")

        category = product_dto.category
        category_exists = category_service.get_by_id(category)
        if not category_exists:
            raise CategoryNotFoundError("Category does not exist.")

        new_product = Product(title=product_dto.title,
                              description=product_dto.description,
                              price=product_dto.price,
                              category=product_dto.category,
                              owner_id=product_dto.owner_id)
        new_product.save()
        return new_product

    def product_update(self, product_id: str, product_dto: ProductDTO):
        try:
            existing_product = self.get_by_id(product_id)
        except ProductNotFoundError:
            return None

        existing_product.modify(title=product_dto.title,
                                description=product_dto.description,
                                price=product_dto.price,
                                owner_id=product_dto.owner_id)
        return existing_product

    def product_delete(self, product_id: str) -> None:
        try:
            existing_product = self.get_by_id(product_id)
        except ProductNotFoundError:
            return None

        existing_product.category_delete()
