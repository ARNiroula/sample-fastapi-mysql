import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext

from config import settings


pwd_context = CryptContext(schemes=["sha256_crypt"])


def hash_password(password: str) -> str:
    return pwd_context.hash(password, scheme="sha256_crypt")


def verify_password(password: str, hashed_pass: str) -> bool:
    return pwd_context.verify(
        secret=password, hash=hashed_pass, scheme="sha256_crypt"
    )


def create_access_token(data: dict) -> str:
    """
    Returns JWT encoded access string of the input

    Parameters:
    data -- dictionary which contains the user_name

    Returns:
    encoded_jwt -- string value
    """
    to_encode = data.copy()

    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, settings.ALGORITHM
    )

    return encoded_jwt


def verify_token_access(token: str, credentials_exception) -> str:
    """
    Verifies the token present in the request headers

    Parameters:
    token -- JWT encoded token

    Returns:
    user_email : str
    """
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_email = payload.get("user_email")

        if user_email is None:
            raise credentials_exception

    except InvalidTokenError:
        raise credentials_exception

    return user_email
