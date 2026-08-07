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

    # 🧱 Create user object (This is your SQLAlchemy model instance)
    new_user = User(
        id=uuid.uuid4(),
        full_name=user_data.full_name,
        email=user_data.email,
        password_hash=hashed_password
    )

    # 💾 Save to DB
    db.add(new_user)  # Adds user to session (not saved yet)
    db.commit()  # Permanently saves to PostgreSQL
    db.refresh(new_user)  # Reloads data from DB (important for getting created_at, etc.)

    return new_user

#compares entered password with hashed password stored in DB
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

#gets user by email from DB
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

# Email exists? → NO → return None  
# Password correct? → NO → return None  
# Else → return user
def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)

    if not user:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user