from marshmallow import Schema, fields, validate


class CategorySchema(Schema):
    id = fields.Str(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(max=50))
    description = fields.Str(required=True)
    owner_id = fields.Str(required=True)


class DeleteCategorySchema(Schema):
    owner_id = fields.Str(required=True)
