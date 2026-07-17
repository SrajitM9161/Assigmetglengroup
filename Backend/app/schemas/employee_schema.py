from marshmallow import Schema, fields, validate


class EmployeeSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=1, max=100))
    role = fields.String(required=True, validate=validate.Length(min=1, max=80))
    availability = fields.Boolean(load_default=True)
