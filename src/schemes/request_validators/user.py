from marshmallow import Schema, fields as marshmallow_fields, validate


class UserCreateRequestValidator(Schema):
    name = marshmallow_fields.String(
        required=True,
        validate=validate.Length(max=255, min=1),
        description="User's name"
    )
    email = marshmallow_fields.Email(
        required=True,
        description="User's email"
    )


class UserUpdateRequestValidator(UserCreateRequestValidator):
    pass
