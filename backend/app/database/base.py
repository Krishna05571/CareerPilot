#This code can be written in the database.py file but 
# Then why make a seperate base.py file
# This is to make the project more model inheritance(if i want to
# change postgreSQL to MySQl i can do it easily) and it also reduces
# coupling ,imporves maintainablity and testability of the code.
from sqlalchemy.orm import DeclarativeBase

#this is also imported into main.py to create tables on startup
class Base(DeclarativeBase):
    pass