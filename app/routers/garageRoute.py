from fastapi import APIRouter, HTTPException, status, Depends
from app import models, schema
from sqlalchemy.orm import Session
from app.database import get_db
from typing import List

router = APIRouter()

# SQLALCHEMY Database buildup
@router.post("/garage/sqlalchemy/", response_model=schema.GarageResponse)
def garage_sqlalchemy(garage: schema.Garage, db: Session = Depends(get_db)):
    # new_car = models.Garage(
    #     name = garage.name,
    #     power = garage.power,
    #     launched = garage.launched
    # )
    new_car = models.Garage(**garage.model_dump())

    db.add(new_car)
    db.commit()
    db.refresh(new_car)
    # return {"New Car details": new_car}
    return new_car

@router.get("/sqlalchemy", response_model = List[schema.Garage])
def get_all(db: Session = Depends(get_db)):
    cars = db.query(models.Garage).all()
    # return {"All Cars": cars}
    return cars

@router.get("/sqlalchemy/{id}")
def get_specific_one(id: int, db: Session = Depends(get_db)):
    car = db.query(models.Garage).filter(models.Garage.id == id ).first()
    if not car:
        raise HTTPException(
            status_code = status.HTTP_204_NO_CONTENT,
            detail = f"Car with the specific id: {id} could not be retrieved."
        )
    # return {"Car details": car}
    return car


@router.put("/garage/sqlalchemy/{id}", response_model = schema.GarageResponse)
def update_function(id: int, garage: schema.Garage, db: Session = Depends(get_db)):
    car_add = db.query(models.Garage).filter(models.Garage.id == id)
    if not car_add: 
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Car addition the specific id: {id} could not be retrieved for update."
        )
    garage_cars= garage.model_dump()   #in car_add we get a pydantic object and model_dump converts it to dictionary because updated only works on dictionary.
    print("Garage Cars informations: ", garage_cars)
    updated_car = car_add.update(garage_cars, synchronize_session = False)
    db.commit()
    # db.refresh(car_add)
    # return {"Car updation": car_add.first()}
    return car_add.first()

@router.delete("/garage/sqlalchemy/{id}")
def deletion_function(id: int, db: Session= Depends(get_db)):
    deleted_car = db.query(models.Garage).filter(models.Garage.id == id)
    if not deleted_car:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Car with the id {id} could not be deleted"
        )
    deleted_car.delete(synchronize_session=False)
    db.commit()
    # return (f"Car with id{id} is deleted")
    return id

@router.patch("/garage/sqlalchemy/{id}", response_model = schema.GarageResponse)
def partial_update(id: int, garage : schema.Garage, db: Session = Depends(get_db)):
    partial_update = db.query(models.Garage).filter(models.Garage.id == id)
    if partial_update.first() is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Car with the id {id} could not be partially updated"
        )
    new_car = garage.model_dump()
    partial_updated_car = partial_update.update(new_car, synchronize_session = False)
    db.commit()
    # return { "message" : f"Partial updation on id {id} is done", "data": partial_update.first()}