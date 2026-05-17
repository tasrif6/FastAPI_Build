from fastapi import APIRouter, HTTPException, status
import psycopg2
from psycopg2.extras import RealDictCursor
from app import models, schema
from app.database import engine

router = APIRouter()

models.Base.metadata.create_all(bind=engine)

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

@router.post("/post", response_model = schema.GarageResponse)
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

@router.get("/")
def get_function():
    return {
        "Allah" : "He is the best planner have faith in him"
    }

@router.get("/details/")
def get_details():
    return {"Learn": "Frontend, Backend, Database properly with build knowledge and then move to agentic buildups."}

@router.get("/garage/{id}")
def get_specific_car(id: int):
    cursor.execute("""select * from garage where car_id = %s """, (str(id), ))
    garage = cursor.fetchone()
    if not garage:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Car with id: {id} not found."
        )
    return {"Car details": garage}
    

@router.delete("/garage/{id}")
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

@router.put("/garage/{id}", response_model = schema.GarageResponse)
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

@router.patch("/garage/{id}", response_model = schema.GarageResponse)
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
