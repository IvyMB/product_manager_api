from marshmallow import Schema, fields, validate, validates_schema, ValidationError
from ..models.role_model import Role


class UserCreateSchema(Schema):
    id = fields.Str(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(max=20))
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
    store_id = fields.Str(required=True)
    roles = fields.List(fields.Str(), validate=validate.Length(min=1), required=True)
    active = fields.Bool(allow_none=True, required=False)

    @validates_schema
    def validate_roles(self, data, **kwargs):
        # Verificar se cada role fornecido existe na tabela Role
        for role_name in data.get('roles', []):
            role_exists = Role.objects(name=role_name).first() is not None
            if not role_exists:
                raise ValidationError(f"Role '{role_name}' doesn't exists.")


class UserUpdateSchema(Schema):
    id = fields.Str(dump_only=True)
    username = fields.Str(required=False, validate=validate.Length(max=20), allow_none=True)
    email = fields.Email(required=False, allow_none=True)
    password = fields.Str(required=False, load_only=True, allow_none=True)
    roles = fields.List(fields.Str(), validate=validate.Length(min=1), required=False, allow_none=True)
    store_id = fields.Str(required=False, allow_none=True)
    active = fields.Bool(allow_none=True, required=False)

    @validates_schema
    def validate_roles(self, data, **kwargs):
        # Verificar se cada role fornecido existe na tabela Role
        for role_name in data.get('roles', []):
            role_exists = Role.objects(name=role_name).first() is not None
            if not role_exists:
                raise ValidationError(f"Role '{role_name}' doesn't exists.")
