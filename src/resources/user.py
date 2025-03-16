from flask import current_app, request
from flask_restx import Namespace, Resource
from marshmallow import ValidationError

from src.dependencies.user_service import get_user_service
from src.exceptions.user import UserNotFoundError
# Request Parsers
from src.schemes.request_parsers.pagination import pagination_parser
from src.schemes.request_parsers.user import user_create_parser, user_update_parser
# Response Parsers
from src.schemes.response_parsers.error import error_model
from src.schemes.response_parsers.user import user_model, user_list_response_model
# DTOs
from src.schemes.dtos.user import CreateUserRequestBody, UpdateUserRequestBody
from src.schemes.dtos.pagination import PaginationParams
# Request Validators
from src.schemes.request_validators.user import UserCreateRequestValidator, UserUpdateRequestValidator


user_ns = Namespace('users')


@user_ns.route("/users/")
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


@user_ns.route("/users/<int:user_id>")
class UserDetailsResource(Resource):
    @user_ns.response(200, "Success", user_model)
    @user_ns.response(404, "User not found")
    def get(self, user_id: int):
        """
        Retrieve details of a specific user
        """
        user_service = get_user_service(current_app.session)

        try:
            user = user_service.get_user_details(user_id)
            return {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "created_at": user.created_at.isoformat(),
            }, 200
        except UserNotFoundError:
            return {"message": "User not found"}, 404

    @user_ns.expect(user_update_parser)
    @user_ns.response(200, "User Updated", user_model)
    @user_ns.response(400, "Invalid user's input", model=error_model)
    @user_ns.response(400, "An Email already taken")
    @user_ns.response(404, "User not found")
    def put(self, user_id: int):
        """
        Updates specific user
        """
        data = request.json
        user_service = get_user_service(current_app.session)

        user_update_schema = UserUpdateRequestValidator()

        try:
            user_update_schema.load(data)
        except ValidationError as err:
            return {"message": err.messages}, 400

        update_user_request_body = UpdateUserRequestBody(
            name=data["name"], email=data["email"]
        )

        try:
            user = user_service.update_user(user_id, update_user_request_body)
            return {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "created_at": user.created_at.isoformat(),
            }, 200
        except UserNotFoundError:
            return {"message": "User not found"}, 404
        except ValueError:
            return {"message": "User with this email already exists"}, 400

    @user_ns.response(204, "User Deleted")
    @user_ns.response(404, "User not found")
    def delete(self, user_id: int):
        """
        Delete specific user
        """
        user_service = get_user_service(current_app.session)
        try:
            user_service.delete_user(user_id)
            return {}, 204
        except UserNotFoundError:
            return {"message": "User not found"}, 404
