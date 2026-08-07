from fastapi import FastAPI
from app.database.database import engine
from app.database.base import Base

#Import all models here 
from app.models.user import User
from app.api.routes import user

app = FastAPI()
#one of the FASTAPI event whenever uvicorn runs this function runs once   
@app.on_event("startup")

def startup():
    # Create all tables in the database
    Base.metadata.create_all(bind=engine)

app.include_router(user.router,prefix = "/api")
@app.get("/")
def root():
    return {
        "message": "CareerPilot Backend Running 🚀"
    }