from flask_restx import fields

from src.extensions import api

pagination_response_model = api.model("PaginationResponseParams", {
    "current_page": fields.Integer(default=1, min=1, description="Page number (must be > 0)"),
    "page_size": fields.Integer(default=15, min=1, description="Number of items per page (must be > 0)"),
    "total_pages": fields.Integer(default=1, min=1, description="Total number of pages"),
    "total_items": fields.Integer(default=1, min=1, description="Total amount of items"),
})
