# Anupreet Singh, anupreet2226579@gmail.com
# Role: Router module for all endpoints that fetch weather data from Open-Meteo

from fastapi import APIRouter, HTTPException
from ..schemas import ForecastResponse, GeoResolved, CurrentWeather, DailyForecastDay
from ..services_open_meteo import geocode, get_current_and_5day

router = APIRouter(prefix="/api/weather", tags=["weather"])# APIRouter Instance

@router.get("/current-forecast", response_model=ForecastResponse)
async def current_and_forecast(query: str):
    """
    query: city, zip, landmark, or 'lat,lon'
    """
    geo = await geocode(query)
    if not geo:
        raise HTTPException(status_code=404, detail="Location not found")

    data = await get_current_and_5day(geo["latitude"], geo["longitude"])
    # Normalize
    current = data.get("current_weather", {})
    daily = data.get("daily", {})
    days = []
    for i, d in enumerate(daily.get("time", [])):
        if i == 0:  # skip today if you prefer “next 5”, or keep; here we keep next 5 including today
            pass
        days.append(DailyForecastDay(
            date=d,
            tmin=daily["temperature_2m_min"][i],
            tmax=daily["temperature_2m_max"][i],
            weathercode=daily["weathercode"][i]
        ))
        if len(days) == 5:
            break

    return ForecastResponse(
        resolved=GeoResolved(**geo),
        current=CurrentWeather(
            temperature=current.get("temperature"),
            windspeed=current.get("windspeed"),
            weathercode=current.get("weathercode"),
            time=current.get("time"),
        ),
        next5days=days
    )
