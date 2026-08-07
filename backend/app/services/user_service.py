from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from passlib.context import CryptContext
import uuid


# 🔐 Password hashing setup (Defines how passwords will be hashed.)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(str(password))


def create_user(db: Session, user_data: UserCreate):
    # 🔒 Hash the password
    hashed_password = hash_password(user_data.password)

    # 🧱 Create user object(This is your SQLAlchemy model instance)
    new_user = User(
        id=uuid.uuid4(),
        full_name=user_data.full_name,
        email=user_data.email,
        password_hash=hashed_password
    )

    # 💾 Save to DB
    db.add(new_user) # Adds user to session (not saved yet)
    db.commit() # Permanently saves to PostgreSQL
    db.refresh(new_user) # Reloads data from DB (important for getting created_at, etc.)

    return new_user