from dataclasses import dataclass


@dataclass
class CreateUserRequestBody:
    name: str
    email: str
