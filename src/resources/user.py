from flask import current_app, request
from flask_restx import Namespace, Resource
from marshmallow import ValidationError

from src.dependencies.user_service import get_user_service
from src.schemes.response_parsers.error import error_model
from src.schemes.request_parsers.pagination import pagination_parser
from src.schemes.request_parsers.user import user_create_parser
from src.schemes.dtos.user import CreateUserRequestBody
from src.schemes.response_parsers.user import user_model, user_list_response_model
from src.schemes.request_validators.user import UserCreateRequestValidator
from src.schemes.dtos.pagination import PaginationParams

user_ns = Namespace('users')


@user_ns.route("/")
class UserResource(Resource):

    @user_ns.expect(pagination_parser)
    @user_ns.marshal_list_with(user_list_response_model)
    def get(self):
        """Retrieve a paginated list of users"""
        params = request.args
        page = int(params.get("page", 1))  # Default page is 1
        page_size = int(params.get("page_size", 15))  # Default page size is 15
        pagination_params = PaginationParams(page, page_size)

        user_service = get_user_service(current_app.session)

        items, pagination_response = user_service.get_user_list(
            pagination_params
        )

        return {
            "items": [
                {"id": item.id, "name": item.name, "email": item.email, "created_at": item.created_at.isoformat()}
                for item in items
            ],
            "pagination": pagination_response.model_dump(),
        }

    @user_ns.expect(user_create_parser)
    @user_ns.response(400, "Wrong email or invalid user's input", model=error_model)
    @user_ns.response(201, "User Created", user_model)
    def post(self):
        """Create a new user"""
        data = request.json
        user_service = get_user_service(current_app.session)

        user_create_schema = UserCreateRequestValidator()

        try:
            user_create_schema.load(data)
        except ValidationError as err:
            return {"message": err.messages}, 400

        create_user_request_body = CreateUserRequestBody(
            name=data["name"], email=data["email"]
        )

        try:
            created_user = user_service.create_user(create_user_request_body)
            return {
                "id": created_user.id,
                "name": created_user.name,
                "email": created_user.email,
                "created_at": created_user.created_at.isoformat(),
            }, 201
        except ValueError as e:
            return {"message": {
                "email": [str(e)],
            }}, 400



@user_ns.route("/<int:user_id>")
class UserDetailsResource(Resource):
    @user_ns.response(200, "Success", user_model)
    @user_ns.response(404, "User not found")
    def get(self, user_id):
        """
        Retrieve details of a specific user
        """
        user_service = get_user_service(current_app.session)

