from marshmallow import Schema, fields as marshmallow_fields, validate


class PaginationParamsValidator(Schema):
    page = marshmallow_fields.Integer(
        required=True,
        validate=validate.Range(min=1),
        description="Page number"
    )
    page_size = marshmallow_fields.Integer(
        required=True,
        validate=validate.Range(min=1),
        description="Items per page"
    )