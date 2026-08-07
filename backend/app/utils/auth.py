# This file creates tokens like JWT (JSON Web Tokens) for user authentication.
# {
#   "sub": "user_email", -> subject of the token (user's email)
#   "exp": expiry_time
# }
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.models.user import User
from jose import JWTError, jwt
import os
from dotenv import load_dotenv

# 🔐 Load environment variables
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 🔑 This tells FastAPI where login happens
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")


# 🔌 DB Dependency (same as before)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 🔐 Create JWT Token
def create_access_token(data: dict):
    to_encode = data.copy()

    # ⏳ Add expiry time
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # 🔏 Encode token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


# 🔓 Decode token + get current user
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials"
    )

    try:
        # 🔓 Decode JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # 📌 Extract user identity
        email: str = payload.get("sub")

        if email is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    # 🔍 Fetch user from DB
    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise credentials_exception

    return user