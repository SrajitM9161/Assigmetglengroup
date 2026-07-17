from marshmallow import Schema, fields, validate, validates_schema, ValidationError


class JobSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=1, max=120))
    startTime = fields.DateTime(required=True, format="iso")
    endTime = fields.DateTime(required=True, format="iso")

    @validates_schema
    def validate_time_range(self, data, **kwargs):
        if data["endTime"] <= data["startTime"]:
            raise ValidationError({"endTime": ["Must be later than startTime."]})
