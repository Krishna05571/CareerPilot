from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import create_user
from app.database.database import SessionLocal

router = APIRouter() # Used to organize endpoints


# 🔌 Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", response_model=UserResponse)# controls what goes back to frontend 
                   #     |-->validates incoming requests
def register_user(user: UserCreate , db: Session = Depends(get_db)):
    return create_user(db, user)   # \-->FastAPI automatically gives a DB session