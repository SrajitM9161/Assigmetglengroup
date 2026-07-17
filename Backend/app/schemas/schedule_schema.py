from marshmallow import Schema, fields


class ScheduleQuerySchema(Schema):
    employeeId = fields.String(required=False)
