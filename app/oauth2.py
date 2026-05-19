import jwt
from datetime import datetime, timedelta, timezone

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

