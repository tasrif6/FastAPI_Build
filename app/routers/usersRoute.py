from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app import models, schema
from app.database import get_db
from app.utils import hash_password

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(users: schema.UsersCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == users.email).first():
        raise HTTPException(400, "Email Already Exists.")
    
    hashed_password = hash_password(users.password)
    users.password = hashed_password
    new_user = models.User(**users.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user