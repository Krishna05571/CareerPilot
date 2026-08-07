from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserResponse, Token, UserLogin
from app.services.user_service import create_user, authenticate_user
from app.database.database import SessionLocal
from app.utils.auth import create_access_token,get_current_user
from app.models.user import User

router = APIRouter()  # Used to organize endpoints


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", response_model=UserResponse)  # controls response
#     |--> validates incoming requests
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)   # -->FastAPI automatically gives DB session


@router.post("/login", response_model=Token)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    db_user = authenticate_user(db, form_data.username, form_data.password)

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token(
        data={"sub": db_user.email, "id": str(db_user.id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user