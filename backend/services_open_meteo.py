# Anupreet Singh, anupreet2226579@gmail.com
# Role: External Weather API(Open-Meteo) Service Layer

import httpx
from typing import Dict, Any, Tuple, Optional, List

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
ARCHIVE_URL  = "https://archive-api.open-meteo.com/v1/archive"  # for date ranges

def parse_query_to_geo_params(query: str) -> Dict[str, Any]:
    """
    Accepts:
      - "lat,lon" -> coordinates
      - ZIP/postal/city/landmark -> use geocoding search
    """
    q = query.strip()
    # quick coordinate check
    if "," in q:
        parts = [p.strip() for p in q.split(",")]
        if len(parts) == 2:
            try:
                lat, lon = float(parts[0]), float(parts[1])
                return {"is_coords": True, "latitude": lat, "longitude": lon}
            except ValueError:
                pass
    return {"is_coords": False, "name": q}

async def geocode(query: str) -> Optional[Dict[str, Any]]:
    params = parse_query_to_geo_params(query)
    if params.get("is_coords"):
        return {
            "name": f"{params['latitude']:.4f},{params['longitude']:.4f}",
            "latitude": params["latitude"],
            "longitude": params["longitude"],
            "country": None,
            "admin1": None
        }
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(GEOCODE_URL, params={"name": params["name"], "count": 1})
        r.raise_for_status()
        data = r.json()
        if not data.get("results"):
            return None
        g = data["results"][0]
        return {
            "name": g.get("name"),
            "latitude": g["latitude"],
            "longitude": g["longitude"],
            "country": g.get("country"),
            "admin1": g.get("admin1"),
        }

async def get_current_and_5day(lat: float, lon: float) -> Dict[str, Any]:
    daily = "weathercode,temperature_2m_max,temperature_2m_min"
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(FORECAST_URL, params={
            "latitude": lat, "longitude": lon,
            "current_weather": True,
            "daily": daily,
            "forecast_days": 7,  # gives us today + a few days; we’ll slice to 5
            "timezone": "auto"
        })
        r.raise_for_status()
        return r.json()

async def get_archive_range(lat: float, lon: float, start_date: str, end_date: str) -> Dict[str, Any]:
    """
    Returns daily min/max temperatures across the date range (inclusive)
    """
    daily = "temperature_2m_max,temperature_2m_min"
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(ARCHIVE_URL, params={
            "latitude": lat, "longitude": lon,
            "start_date": start_date, "end_date": end_date,
            "daily": daily,
            "timezone": "auto"
        })
        r.raise_for_status()
        return r.json()

def map_weathercode_to_emoji(code: int) -> str:
    # (Keep server-side in case you want to reuse on exports)
    # Minimal mapping: https://open-meteo.com/en/docs
    if code == 0: return "☀️"
    if code in (1,2): return "🌤️"
    if code == 3: return "☁️"
    if code in (45,48): return "🌫️"
    if code in (51,53,55,56,57): return "🌦️"
    if code in (61,63,65,66,67): return "🌧️"
    if code in (71,73,75,77): return "❄️"
    if code in (80,81,82): return "🌧️"
    if code in (95,96,99): return "⛈️"
    return "🌡️"
