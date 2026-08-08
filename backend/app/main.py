from fastapi import FastAPI
from app.database.database import engine
from app.database.base import Base
from fastapi.middleware.cors import CORSMiddleware
#Import all models here 
from app.models.user import User
from app.api.routes import user
from app.api.routes import resume


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#one of the FASTAPI event whenever uvicorn runs this function runs once   
@app.on_event("startup")

def startup():
    # Create all tables in the database
    Base.metadata.create_all(bind=engine)

app.include_router(user.router,prefix = "/api")

app.include_router(resume.router,prefix = "/api",tags=["Resume"])

@app.get("/")
def root():
    return {
        "message": "CareerPilot Backend Running 🚀"
    }