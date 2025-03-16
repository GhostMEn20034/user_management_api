from dataclasses import dataclass


@dataclass
class CreateUserRequestBody:
    name: str
    email: str


@dataclass
class UpdateUserRequestBody(CreateUserRequestBody):
    pass
