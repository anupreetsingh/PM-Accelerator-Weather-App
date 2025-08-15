# Anupreet Singh, anupreet2226579@gmail.com
# Role: Database Operations Layer (CRUD)

from sqlalchemy.orm import Session
from . import models

def get_or_create_location(db: Session, geo: dict) -> models.Location:
    existing = db.query(models.Location).filter(
        models.Location.latitude == geo["latitude"],
        models.Location.longitude == geo["longitude"]
    ).first()
    if existing:
        return existing
    loc = models.Location(
        name=geo.get("name"),
        latitude=geo["latitude"],
        longitude=geo["longitude"],
        country=geo.get("country"),
        admin1=geo.get("admin1"),
        source="open-meteo",
    )
    db.add(loc)
    db.commit()
    db.refresh(loc)
    return loc

def create_request(db: Session, location_id: int, start_date, end_date, payload):
    row = models.WeatherRequest(
        location_id=location_id, start_date=start_date, end_date=end_date, payload=payload
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row

def list_requests(db: Session):
    requests = db.query(models.WeatherRequest).order_by(models.WeatherRequest.id.desc()).all()
    # Add location details to each request
    for request in requests:
        if request.location:
            request.location_name = request.location.name
            request.location_country = request.location.country
            request.location_admin1 = request.location.admin1
            request.location_coords = f"{request.location.latitude:.4f}, {request.location.longitude:.4f}"
    return requests

def get_request(db: Session, rid: int):
    request = db.query(models.WeatherRequest).filter(models.WeatherRequest.id == rid).first()
    if request and request.location:
        request.location_name = request.location.name
        request.location_country = request.location.country
        request.location_admin1 = request.location.admin1
        request.location_coords = f"{request.location.latitude:.4f}, {request.location.longitude:.4f}"
    return request

def update_request_dates(db: Session, rid: int, start_date=None, end_date=None):
    row = get_request(db, rid)
    if not row: return None
    if start_date: row.start_date = start_date
    if end_date: row.end_date = end_date
    db.commit()
    db.refresh(row)
    return row

def delete_request(db: Session, rid: int):
    row = get_request(db, rid)
    if not row: return False
    db.delete(row)
    db.commit()
    return True
