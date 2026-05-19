import jwt
from datetime import datetime, timedelta, timezone
from . import schema
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from . import models, schema, database
from sqlalchemy.orm import Session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "login")

SECRET_KEY = "4ea1b88667eaed38b12798d9012c683dfaec15f4f3232733a88641f3d55f054b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta : timedelta | None = None):
    to_encode = data.copy()
    if expires_delta: 
        expire = datetime.now(timezone.utc) + expires_delta
    else: 
        expire = datetime.now(timezone.utc) + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp" : expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)

    return encode_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = schema.TokenData(id = id)

    except InvalidTokenError:
        raise credentials_exception
     
    return token_data


def current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate credentials",
        headers = {"WWW-Authenticate": "Bearer"},
    )

    token= verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id ).first()

    return user

