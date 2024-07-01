from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from jwt import InvalidTokenError
from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from deps import DBSession
from auth import (
    create_access_token,
    create_reset_password_token,
    hash_password,
    verify_password,
    decode_reset_password_token
)
from models.models import Users
from schemas.users import UserRegister
from config import settings


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


@router.post("/forget-password")
async def forget_password(
    request: Request,
    email: str,
    session: DBSession
):
    query = select(Users).where(Users.email == email)
    result = await session.execute(query)
    try:
        user = result.scalar_one()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User Not Found, Error {e}"
        )

    secret_token = create_reset_password_token(user.email)
    forgot_url_link = f"{request.base_url}/users/reset_password?access_token={secret_token}"  # noqa

    message = Mail(
        from_email="testanuptest777@gmail.com",
        to_emails=user.email,
        subject="Test",
        html_content="<strong>" + forgot_url_link + "</strong>"
    )

    # try:
    sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
    res = sg.send(message)
    print(res)
    print(res.body)
    print(res.status_code)
    print(res.headers)
    # except Exception as e:
    #     raise HTTPException(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         detail=f"Error -> {e} when sending email"
    #     )

    return {
        "result": f"An email has been sent to {user.email} with a link for password reset"  # noqa
    }


@router.post("/reset_password")
async def reset_password(
    # curr_user: CURR_USER,
    new_password: str,
    session: DBSession,
    secret_token: str = Query()
):
    try:
        email = decode_reset_password_token(secret_token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Token"
        )
    # if email != curr_user.email:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Invalid Email Address",
    #     )

    ddl = update(Users)\
        .where(Users.email == email)\
        .values(password=hash_password(new_password))

    await session.execute(ddl)
    await session.commit()

    return {"status": "Password has been successfully reset", "success": True}
