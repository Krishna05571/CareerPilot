from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
import uuid


# 🔹 Schema for user registration (request)
class UserCreate(BaseModel):#Validate Incoming Data
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)
# ... -> this means that this field is required 

# 🔹 Schema for API response (what we send back)
class UserResponse(BaseModel):
    id: uuid.UUID
    full_name: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True # This means you can convert 
        #SQLAlchemy objects to JSON response 
        #without his FastAPI cannot return DB objects properly