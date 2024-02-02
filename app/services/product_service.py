from ..models import Product
from ..dtos import ProductDTO
from .category_service import CategoryService
from app.exceptions.category_exceptions import CategoryNotFoundError
from app.exceptions import ProductAlreadyExistsError, ProductNotFoundError
import logging


class ProductService:
    def get_by_id(self, product_id: str):
        product = Product.objects(id=product_id).first()
        if not product:
            raise ProductNotFoundError
        return product

    def check_product_exists_for_owner(self, title: str, owner_id: str):
        product = Product.objects(owner_id=owner_id, title=title).first()
        return product

    def get_product_by_owner_id(self, owner_id: str,  product_id: str):
        product = Product.objects(owner_id=owner_id, id=product_id).first()
        if not product:
            raise ProductNotFoundError
        return product

    def get_all(self):
        all_products = Product.objects()
        return all_products

    def create(self, product_dto: ProductDTO, category_service: CategoryService):
        product_exists = self.check_product_exists_for_owner(title=product_dto.title, owner_id=product_dto.owner_id)
        if product_exists:
            raise ProductAlreadyExistsError

        try:
            category_service.get_by_id(category_id=product_dto.category)
        except CategoryNotFoundError:
            raise CategoryNotFoundError

        new_product = Product(title=product_dto.title,
                              description=product_dto.description,
                              price=product_dto.price,
                              category=product_dto.category,
                              owner_id=product_dto.owner_id)
        new_product.save()
        return new_product

    def product_update(self, product_id: str, product_dto: ProductDTO):
        try:
            existing_product = self.get_product_by_owner_id(product_id, product_dto.owner_id)
        except ProductNotFoundError:
            return None

        existing_product.update(title=product_dto.title,
                                description=product_dto.description,
                                price=product_dto.price,
                                owner_id=product_dto.owner_id)
        return existing_product

    def product_delete(self, product_id: str, product_data: dict[str]) -> bool:
        owner_id = product_data['owner_id']
        try:
            product = self.get_product_by_owner_id(product_id=product_id, owner_id=owner_id)
        except ProductNotFoundError:
            return False

        product.delete()
        return True
