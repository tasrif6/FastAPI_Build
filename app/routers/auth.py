from fastapi import APIRouter, status, HTTPException, Depends, responses
from sqlalchemy.orm import Session
from .. import database, models, utils, schema, oauth2
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(tags =["Login Authentication"])

@router.post('/login')
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db), get_current_user: int = Depends(oauth2.current_user)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND, detail = "Invalid Credentials"
        )
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code = status.HTTP_406_NOT_ACCEPTABLE, detail = "Invalid Password"
        )

    access_token = oauth2.create_access_token(
        data = {"user_id" : user.id},
        expires_delta = timedelta(minutes = oauth2.ACCESS_TOKEN_EXPIRE_MINUTES)
    ) 
    return {"Access_token": access_token, "token_type": "bearer"}