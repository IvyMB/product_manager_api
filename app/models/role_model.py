from mongoengine import Document, StringField


class Role(Document):
    name = StringField(required=True, unique=True)

    meta = {'collection': 'role'}
