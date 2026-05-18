from fastapi import FastAPI
from . routers import garageRoute, usersRoute, basicModel, auth

# main object calling for class
app = FastAPI()

app.include_router(garageRoute.router)
app.include_router(usersRoute.router)
app.include_router(basicModel.router)
app.include_router(auth.router)









