# Anupreet Singh, anupreet2226579@gmail.com
# Role: Data Validation and API Schema Definitions

from datetime import date
from pydantic import BaseModel, Field, model_validator 
from typing import Optional, Any, List

# ----- Core DTOs -----
class GeoResolved(BaseModel): # When you inherit BaseModel into a class it becomes a Pydantic Model/schema/DTO
    name: str
    latitude: float
    longitude: float
    country: Optional[str] = None
    admin1: Optional[str] = None

class CurrentWeather(BaseModel):
    temperature: float
    windspeed: float
    weathercode: int
    time: str

class DailyForecastDay(BaseModel):
    date: str
    tmin: float
    tmax: float
    weathercode: int

class ForecastResponse(BaseModel):
    resolved: GeoResolved
    current: CurrentWeather
    next5days: List[DailyForecastDay]

# ----- CRUD DTOs -----
class RequestCreate(BaseModel):
    query: str = Field(..., description="City/ZIP/coords/landmark")
    start_date: date
    end_date: date

    @model_validator(mode="after")
    def check_dates(self):
        if self.end_date < self.start_date:
            raise ValueError("end_date must be >= start_date")
        return self

class RequestUpdate(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None

    @model_validator(mode="after")
    def check_dates(self):
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValueError("end_date must be >= start_date")
        return self

class RequestRow(BaseModel):
    id: int
    location_id: int
    start_date: date
    end_date: date
    payload: Any
    # Include location details
    location_name: Optional[str] = None
    location_country: Optional[str] = None
    location_admin1: Optional[str] = None
    location_coords: Optional[str] = None
    class Config:
        from_attributes = True
