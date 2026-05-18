from pydantic import BaseModel, EmailStr
from datetime import date


#define request body schema
class Garage(BaseModel):
    name: str
    power: str
    launched: date

class GarageUpdate(BaseModel):
    car_id: int | None = None
    name: str | None = None
    power: str | None = None
    launched: date | None = None

class GarageResponse(Garage):
    id : int
    
    class Config:
        orm_model = True


class UsersCreate(BaseModel):
    email : EmailStr 
    password: str

class Login(BaseModel):
    email: EmailStr
    password: str