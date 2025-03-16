from flask_restx import fields

from src.extensions import api
from src.schemes.response_parsers.pagination import pagination_response_model

user_model = api.model('User', {
    "id": fields.Integer(readOnly=True),
    "name": fields.String(required=True, max_length=255),
    "email": fields.String(required=True, max_length=255),
    "created_at": fields.DateTime(readOnly=True),
})
user_list_response_model = api.model(
    "UserListResponse",
    {
        "items": fields.List(fields.Nested(user_model), description="List of users"),
        "pagination": fields.Nested(pagination_response_model, description="Pagination metadata"),
    },
)
