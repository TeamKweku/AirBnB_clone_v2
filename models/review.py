#!/usr/bin/python3
""" Review module for the HBNB project """
# from models.place import Place
# from models.user import User
from models.base_model import BaseModel, Base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from models.place import Place
from models.user import User
import os


storage_type = os.getenv('HBNB_TYPE_STORAGE')
class Review(BaseModel, Base):
    """ Review classto store review information """
    __tablename__ = "reviews"
    if storage_type == "db":
        text = Column(String(1024), nullable=False)
        place_id = Column(String(60), ForeignKey("places.id"), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    else:
        place_id = ""
        user_id = ""
        text = ""
