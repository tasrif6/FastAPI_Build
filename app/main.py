from fastapi import FastAPI, HTTPException, status, Response, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models, schema, utils
from sqlalchemy.orm import Session
from . database import engine, get_db
from typing import List

# main object calling for class
app = FastAPI()

models.Base.metadata.create_all(bind= engine)


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

@app.post("/post", response_model = schema.GarageResponse)
def create_post(post: schema.Garage):
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

@app.put("/garage/{id}", response_model = schema.GarageResponse)
def update_car(id: int, garage: schema.Garage):
    cursor.execute("""update garage set name=%s, power = %s, launched=%s where car_id = %s Returning * """,(garage.name, garage.power, garage.launched, str(id)))
    updated_car = cursor.fetchone()
    connected.commit()
    if updated_car == None:
        raise HTTPException(
            status_code = status.HTTP_204_NO_CONTENT,
            detail = f"Course with car id: {id} doesn't exists"
        )
    return {"data": updated_car}

@app.patch("/garage/{id}", response_model = schema.GarageResponse)
def partial_update(id:int, garage: schema.Garage):
    cursor.execute(""" update garage set name =%s, power = %s, launched= %s where car_id = %s Returning * """, (garage.name, garage.power, garage.launched, str(id)))
    partially_updated_car = cursor.fetchone()
    connected.commit()
    if partially_updated_car == None:
        raise HTTPException(
            status_code =  status.HTTP_204_NO_CONTENT,
            detail = f"Car name with id: {id} could not be changed."
        )
    return {"New data": partially_updated_car}




#=================================================================================================================================================================================
#SQLALCHEMY Database buildup 
@app.post("/garage/sqlalchemy/", response_model = schema.GarageResponse)
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

@app.get("/sqlalchemy", response_model = List[schema.Garage])
def get_all(db: Session = Depends(get_db)):
    cars = db.query(models.Garage).all()
    # return {"All Cars": cars}
    return cars

@app.get("/sqlalchemy/{id}")
def get_specific_one(id: int, db: Session = Depends(get_db)):
    car = db.query(models.Garage).filter(models.Garage.id == id ).first()
    if not car:
        raise HTTPException(
            status_code = status.HTTP_204_NO_CONTENT,
            detail = f"Car with the specific id: {id} could not be retrieved."
        )
    # return {"Car details": car}
    return car


@app.put("/garage/sqlalchemy/{id}", response_model = schema.GarageResponse)
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

@app.delete("/garage/sqlalchemy/{id}")
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

@app.patch("/garage/sqlalchemy/{id}", response_model = schema.GarageResponse)
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


#=============================================================================================================================================
@app.post("/users", status_code = status.HTTP_201_CREATED)
def create_user(users: schema.UsersCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == users.email).first():
        raise HTTPException(400, "Email Already Exists.")
    hashed_password = utils.hash_password(users.password)
    users.password = hashed_password
    new_user = models.User(**users.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user