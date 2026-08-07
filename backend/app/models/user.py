# WHY WE NEED THIS FILE???
# user.py defines the structure of the users table in PostgreSQL 
# using a Python class.
# SQLAlchemy uses this model to create, read, update, and delete 
# user records without writing raw SQL queries.

# SQLAlchemy acts as a translator 
# py object -> SQLAlchemy ORM -> PostgreSQL table
# ORM - Object Relational Mappers

import uuid
#so that we can use UUID as primary key for user table
#and it makes it more secure as guessing it becomes tougher instead of intergers

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.database.base import Base


class User(Base):
    __tablename__ = "users"
#MAPPED func tells what type of field is stored in the col
    id: Mapped[uuid.UUID] = mapped_column(#every field inside the class becomes a col
        primary_key=True,
        default=uuid.uuid4
        #this makes sure that every time a new user is created a new
        #unique UUID is generated automatically 
    )

    full_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),#VARCHAR(255)
        nullable=False
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()#used instead of current_timestamp()
        #because it is timezone aware ,more acc,works even if another service inserts data
    )