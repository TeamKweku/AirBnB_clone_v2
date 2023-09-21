#!/usr/bin/python3
""" State Module for HBNB project """
import os
import models
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, relationship

class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"

    if os.getenv('HBNB_TYPE_STORAGE') == "db":
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state", cascade="all, delete")

    else:
        name = ""
        @property
        def cities(self):
            """ returns the list of `City`instances with `state_id` equals to the
            current `State.id`.
            it will be the FileStorage relationship between`State` and `City`
            """
            city_list = []
            for city in storage.all(City).values():
               if city.state_id == self.id:
                   city_list.append(city)
            return city_list
