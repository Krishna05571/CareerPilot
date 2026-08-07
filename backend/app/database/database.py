# this file is basically a bridge between fastapi and PostgreSql

# whats the main work of this file  
# creates the database engine
# opens database session
# closes the automatically after the request is completed
# creates a base class that every model will inherit from


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.core.config import DATABASE_URL

#Database Engine imported in main.py to create tables on startup   
engine = create_engine(
    DATABASE_URL,
    echo=True # TRUE->Print every SQL Query ... later will change to FALSE 
    )

#Database Session Factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

#Dependency function to get a database session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()