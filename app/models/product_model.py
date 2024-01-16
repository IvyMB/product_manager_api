from mongoengine import Document, StringField, FloatField, ReferenceField, ObjectIdField
from .category_model import Category


class Product(Document):
    title = StringField(required=True, max_length=50)
    description = StringField(required=True, max_length=500)
    category = ReferenceField(Category)
    price = FloatField(required=True)
    owner_id = StringField(required=True)

    meta = {'collection': 'product'}
