from marshmallow import Schema, fields, validate


class UserCreateSchema(Schema):
    id = fields.Str(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(max=20))
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
    store_id = fields.Str(required=True)
    active = fields.Bool(allow_none=True, required=False)


class UserUpdateSchema(Schema):
    id = fields.Str(dump_only=True)
    username = fields.Str(required=False, validate=validate.Length(max=20), allow_none=True)
    email = fields.Email(required=False, allow_none=True)
    password = fields.Str(required=False, load_only=True, allow_none=True)
    store_id = fields.Str(required=False, allow_none=True)
    active = fields.Bool(allow_none=True, required=False)
