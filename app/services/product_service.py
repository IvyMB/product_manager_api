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
            return None
        return product

    def get_all(self):
        all_products = Product.objects()
        return all_products

    def create(self, product_dto: ProductDTO):
        new_product = Product(title=product_dto.title,
                              description=product_dto.description,
                              price=product_dto.price,
                              category=product_dto.category,
                              owner_id=product_dto.owner_id)
        new_product.save()
        return new_product

    def update_product(self, product_id: str, product_dto: ProductDTO):
        existing_product = self.get_product_by_owner_id(product_id, product_dto.owner_id)
        if not existing_product:
            raise ProductNotFoundError

        existing_product.update(title=product_dto.title,
                                description=product_dto.description,
                                price=product_dto.price,
                                owner_id=product_dto.owner_id)
        return existing_product

    def delete_product(self, product_id: str, owner_id: str) -> bool:
        product = self.get_product_by_owner_id(product_id=product_id, owner_id=owner_id)
        if not product:
            raise ProductNotFoundError

        product.delete()
        return True
