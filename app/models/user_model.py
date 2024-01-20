from mongoengine import Document, StringField, EmailField, BooleanField


class User(Document):
    username = StringField(required=True, max_length=20)
    email = EmailField(required=True)
    password = StringField(required=True)
    store_id = StringField(required=True)
    active = BooleanField(default=True)

    meta = {'collection': 'user'}
