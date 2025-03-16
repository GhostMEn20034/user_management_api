from flask_restx import fields

from src.extensions import api

error_model = api.model(
    "ErrorModel",
    {
        "message": fields.Raw(
            description="Error message, can be a string or a dictionary of field errors",
            example={
                "email": ["Email already exists", ],
            }
        ),
    },
)
