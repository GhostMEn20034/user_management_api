from flask_restx import reqparse

pagination_parser = reqparse.RequestParser()
pagination_parser.add_argument(
    "page", type=int,
    default=1,
    location="args",
    help="Page number (must be > 0)")

pagination_parser.add_argument(
    "page_size",
    type=int,
    default=15,
    location="args",
    help="Number of items per page (must be > 0)"
)

