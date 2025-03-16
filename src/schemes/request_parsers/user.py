from flask_restx import reqparse, inputs


# Define a request parser
user_create_parser = reqparse.RequestParser()
user_create_parser.add_argument(
    "name",
    type=str,
    required=True,
    help="User's name (max length: 255)",
    location="json"
)
user_create_parser.add_argument(
    "email",
    type=inputs.email(check=True),
    required=True,
    help="User's email",
    location="json"
)