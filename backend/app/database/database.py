# this file is basically a bridge between fastapi and PostgreSql

# whats the main work of this file  
# creates the database engine
# opens database session
# closes the automatically after the request is completed
# creates a base class that every model will inherit from


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import DATABASE_URL

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()