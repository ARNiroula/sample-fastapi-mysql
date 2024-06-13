from typing import Annotated
from pydantic import BaseModel, EmailStr, constr


class UserBase(BaseModel):
    user_email: EmailStr


class UserRegister(UserBase):
    password: Annotated[str, constr(min_length=4)]


class UserGet(UserBase):
    pass
