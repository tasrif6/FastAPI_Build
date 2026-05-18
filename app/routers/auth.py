from fastapi import APIRouter, status, HTTPException, Depends, responses
from sqlalchemy.orm import Session
from .. import database, models, utils, schema

router = APIRouter(tags =["Login Authentication"])

@router.post('/login')
def login(user_credentials: schema.Login, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    if not user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND, detail = "Invalid Credentials"
        )
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND, detail = "Invalid Credentials"
        )
    return {"token": "Successfully login"}