# Anupreet Singh, anupreet2226579@gmail.com
# Role: Database Models and Table Definitions

from sqlalchemy import Column, Integer, String, Float, Date, JSON, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base # From db.py file import the Base object from it 

class Location(Base):# Every Class that inherits Base becomes a mapped class. 
    __tablename__ = "locations" # Name of the table that will be created in the database
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)            # e.g., "Vancouver, CA"
    latitude = Column(Float, index=True)
    longitude = Column(Float, index=True)
    country = Column(String, nullable=True)
    admin1 = Column(String, nullable=True)       # state/province
    source = Column(String, default="open-meteo")

    requests = relationship("WeatherRequest", back_populates="location")

class WeatherRequest(Base):
    __tablename__ = "weather_requests"
    id = Column(Integer, primary_key=True, index=True)
    location_id = Column(Integer, ForeignKey("locations.id"))
    start_date = Column(Date)
    end_date = Column(Date)
    # Store the exact response slice (daily temps, metadata)
    payload = Column(JSON)

    location = relationship("Location", back_populates="requests")
