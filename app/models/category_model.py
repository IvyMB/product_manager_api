from mongoengine import Document, StringField


class Category(Document):
    title = StringField(required=True)
    description = StringField(required=True)
    owner_id = StringField(required=True)

    meta = {'collection': 'category'}
