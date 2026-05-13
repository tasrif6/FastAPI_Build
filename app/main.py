from fastapi import FastAPI, HTTPException, status, Response, Depends
from pydantic import BaseModel, HttpUrl
from datetime import date
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models
from sqlalchemy.orm import Session
from . database import engine, get_db


# main object calling for class
app = FastAPI()

models.Base.metadata.create_all(bind= engine)

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

#Database connection setup
while True:
    try:
        connected = psycopg2.connect(host = "localhost", database = "FastAPI_Learning", user= "postgres", password = "123456", cursor_factory = RealDictCursor)
        cursor = connected.cursor()
        print("Database connected successfully")
        break

    except Exception as error:
        print("Database connection failed")
        print("Error message: ", error)
        break
        
# def retrive_data():
#     cursor.execute("""select * from garage""")
#     data = cursor.fetchall()
#     print(data)

@app.post("/post")
def create_post(post: Garage):
    try:
        cursor.execute(""" Insert into garage(name, power, launched) values (%s, %s, %s) Returning * """, (post.name, post.power, post.launched))
        new_post = cursor.fetchone()
        connected.commit()
        return {"data" : new_post}
    except Exception as e:
        connected.rollback()
        raise HTTPException(status_code=500, detail=str(e))
        # return {"error at inserting: ", error}

@app.get("/")
def get_function():
    return {
        "Allah" : "He is the best planner have faith in him"
    }

@app.get("/details/")
def get_details():
    return {"Learn": "Frontend, Backend, Database properly with build knowledge and then move to agentic buildups."}

@app.get("/garage/{id}")
def get_specific_car(id: int):
    cursor.execute("""select * from garage where car_id = %s """, (str(id), ))
    garage = cursor.fetchone()
    if not garage:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Car with id: {id} not found."
        )
    return {"Car details": garage}
    

@app.delete("/garage/{id}")
def delete_car(id: int):
    cursor.execute("""delete from garage where car_id = %s Returning * """, (str(id), ))
    deleted_car = cursor.fetchone()
    connected.commit()
    if deleted_car == None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Car with the specific id: {id} could not be deleted"
        )
    return (f"message: Car is deleted")

@app.put("/garage/{id}")
def update_car(id: int, garage: Garage):
    cursor.execute("""update garage set name=%s, power = %s, launched=%s where car_id = %s Returning * """,(garage.name, garage.power, garage.launched, str(id)))
    updated_car = cursor.fetchone()
    connected.commit()
    if updated_car == None:
        raise HTTPException(
            status_code = status.HTTP_204_NO_CONTENT,
            detail = f"Course with car id: {id} doesn't exists"
        )
    return {"data": updated_car}

@app.patch("/garage/{id}")
def partial_update(id:int, garage: Garage):
    cursor.execute(""" update garage set name =%s, power = %s, launched= %s where car_id = %s Returning * """, (garage.name, garage.power, garage.launched, str(id)))
    partially_updated_car = cursor.fetchone()
    connected.commit()
    if partially_updated_car == None:
        raise HTTPException(
            status_code =  status.HTTP_204_NO_CONTENT,
            detail = f"Car name with id: {id} could not be changed."
        )
    return {"New data": partially_updated_car}


#SQLALCHEMY Database buildup 
@app.post("/garage/sqlachemy/")
def garage_sqlalchemy(garage: Garage, db: Session = Depends(get_db)):
    new_car = models.Garage(
        name = garage.name,
        power = garage.power,
        launched = garage.launched
    )

    db.add(new_car)
    db.commit()
    db.refresh(new_car)
    return {"New Car details": new_car}

@app.get("/sqlalchemy")
def get_all(db: Session = Depends(get_db)):
    cars = db.query(models.Garage).all()
    return {"All Cars": cars}

@app.get("/sqlalchemy/{id}")
def get_specific_one(id: int, db: Session = Depends(get_db)):
    car = db.query(models.Garage).filter(models.Garage.id == id ).first()
    if not car:
        raise HTTPException(
            status_code = status.HTTP_204_NO_CONTENT,
            detail = f"Car with the specific id: {id} could not be retrieved."
        )
    return {"Car details": car}
