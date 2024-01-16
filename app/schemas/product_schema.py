from marshmallow import Schema, fields, validate


class ProductSchema(Schema):
    id = fields.Str(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(max=50))
    description = fields.Str(required=True, validate=validate.Length(max=500))
    category = fields.Str(required=True, attribute='category.id')
    price = fields.Str(required=True)
    owner_id = fields.Str(required=True)
