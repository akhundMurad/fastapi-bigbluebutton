from typing import Optional

from pydantic import BaseModel, root_validator, validator

from src.db.choices import UserRoleChoices


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class UserRead(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    role: str

    class Config:
        orm_mode = True


class UserRegister(BaseModel):
    username: str
    first_name: str
    last_name: str
    role: str
    raw_password1: str
    raw_password2: str

    @validator("role")
    def check_role_in_choices(cls, v):
        assert v in UserRoleChoices.values()
        return v

    @root_validator
    def check_passwords_match(cls, values):
        pw1, pw2 = values.get("password1"), values.get("password2")
        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError("passwords do not match")
        return values


class UserCreate(BaseModel):
    username: str
    first_name: str
    last_name: str
    role: str
    password: str
