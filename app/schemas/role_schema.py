from marshmallow import Schema, fields, validate


class RoleSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
