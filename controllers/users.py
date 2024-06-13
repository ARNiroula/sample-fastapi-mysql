from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from deps import DBSession
from auth import create_access_token, hash_password, verify_password
from models.models import Users
from schemas.users import UserRegister


router = APIRouter(
    prefix="/user",
    tags=["Users"]
)


@router.post("/register")
async def register_user(user_data: UserRegister, session: DBSession):
    new_user = Users(
        email=user_data.user_email,
        password=hash_password(user_data.password)
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return {"Users Registered"}


@router.post("/login")
async def login_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: DBSession
):
    query = select(Users).where(Users.email == form_data.username)
    result = await session.execute(query)

    try:
        one_user = result.scalar_one()
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found!"
        )

    if not verify_password(form_data.password, one_user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid credentials"
        )

    token_input = {
        "access_token": create_access_token(
            {"user_email": one_user.email}
        ),
        "token_type": "bearer"
    }

    return token_input
