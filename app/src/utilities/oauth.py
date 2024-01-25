from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from decouple import config
from typing import Union
from datetime import timedelta, datetime
from typing_extensions import Annotated

from src.database.connection import UserConnection
from src.utilities.security_pw import SecurityPassword

secure_pw = SecurityPassword()
userconn = UserConnection()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/application/api/ver/v1/authentication/auth")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credential_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate the token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            config("SECRET_KEY"),
            algorithms=[config("ALGORITHM")],  # Enforce specific algorithm
        )
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token format")
    except JWTError:
        raise credential_exc

    user = userconn.get_user(username=username)
    if not user:
        raise credential_exc

    # Additional security checks:
    if not jwt.get_unverified_header(token).get("alg") == config("ALGORITHM"):
        raise credential_exc  # Verify algorithm in header

    # Consider:
    # - Checking token expiration
    # - Verifying token issuer (if applicable)
    # - Implementing additional validation based on your specific requirements

    return user

    
async def authenticate_user(username: str, password: str):
    user = userconn.get_user(username)
    #print(user.username)
    if not user:
        return None
    if not secure_pw.verify_password(password, user.password):
        return False
    
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Creates a secure access token with enhanced security measures.

    Args:
        data: The payload data to be included in the token.
        expires_delta: The timedelta for token expiration. Defaults to 30 minutes.

    Returns:
        The encoded JWT access token.
    """

    to_encode = data.copy()

    # Ensure a default expiration time if not provided
    expires = datetime.now() + expires_delta if expires_delta else datetime.now() + timedelta(minutes=30)

    to_encode.update({"exp": expires})  # Add expiration time

    # Use a secure algorithm and enforce it during encoding
    algorithm = config("ALGORITHM")
    secret_key = config("SECRET_KEY")

    encoded_jwt_token = jwt.encode(
        to_encode,
        secret_key,
        algorithm=algorithm,
        headers={"alg": algorithm},  # Include algorithm header
    )

    return encoded_jwt_token