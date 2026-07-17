from marshmallow import Schema, fields


class AssignmentSchema(Schema):
    employeeId = fields.String(required=True)
    jobId = fields.String(required=True)
