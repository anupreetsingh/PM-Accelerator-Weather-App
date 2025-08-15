# Anupreet Singh, anupreet2226579@gmail.com
# Role: Router Module for all endpoints that store or retrieve records from database

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from ..db import get_db
from .. import crud
from ..schemas import RequestCreate, RequestUpdate, RequestRow
from ..services_open_meteo import geocode, get_archive_range

router = APIRouter(prefix="/api/records", tags=["records"]) # APIRouter Instance

@router.post("", response_model=RequestRow)
async def create_record(payload: RequestCreate, db: Session = Depends(get_db)):
    geo = await geocode(payload.query)
    if not geo:
        raise HTTPException(status_code=404, detail="Location not found (or ambiguous)")

    # Fetch temps for the date range (daily min/max)
    wx = await get_archive_range(
        geo["latitude"], geo["longitude"],
        start_date=str(payload.start_date),
        end_date=str(payload.end_date)
    )
    # Basic sanity: expect 'daily' keys
    if "daily" not in wx or "time" not in wx["daily"]:
        raise HTTPException(status_code=502, detail="Weather archive unavailable for this range")

    loc = crud.get_or_create_location(db, geo)
    row = crud.create_request(
        db, loc.id, payload.start_date, payload.end_date, payload=wx["daily"]
    )
    return row

@router.get("", response_model=list[RequestRow])
def list_records(db: Session = Depends(get_db)):
    return crud.list_requests(db)

@router.get("/{rid}", response_model=RequestRow)
def read_record(rid: int, db: Session = Depends(get_db)):
    row = crud.get_request(db, rid)
    if not row:
        raise HTTPException(status_code=404, detail="Record not found")
    return row

@router.patch("/{rid}", response_model=RequestRow)
async def update_record(rid: int, body: RequestUpdate, db: Session = Depends(get_db)):
    row = crud.get_request(db, rid)
    if not row:
        raise HTTPException(status_code=404, detail="Record not found")

    # If dates are changing, refetch archive
    start = body.start_date or row.start_date
    end = body.end_date or row.end_date
    wx = await get_archive_range(
        row.location.latitude, row.location.longitude,
        start_date=str(start), end_date=str(end)
    )
    if "daily" not in wx or "time" not in wx["daily"]:
        raise HTTPException(status_code=502, detail="Weather archive unavailable for this range")

    updated = crud.update_request_dates(db, rid, body.start_date, body.end_date)
    # overwrite payload
    updated.payload = wx["daily"]
    db.commit()
    db.refresh(updated)
    return updated

@router.delete("/{rid}")
def delete_record(rid: int, db: Session = Depends(get_db)):
    ok = crud.delete_request(db, rid)
    if not ok:
        raise HTTPException(status_code=404, detail="Record not found")
    return {"status": "deleted", "id": rid}
