from pydantic import BaseModel


class AuthUser(BaseModel):
    username: str
    password: str | None = None


class SignUpUser(AuthUser):
    email: str


class Tokens(BaseModel):
    access_token: str
    refresh_token: str
