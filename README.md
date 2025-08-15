# 🌤️ Weather App

## Steps to Run the App

Step 1. **Cd project directory**
   ```bash
   cd PM-Accelerator-Weather-App-main
   ```

Step 2. **python setup.py**
   ```bash
   python setup.py
   ```

Step 3. **uvicorn backend.main:app --reload**
   ```bash
   uvicorn backend.main:app --reload
   ```

Step 4. **Open "frontend/index.html" in web browser**
   - Open `frontend/index.html` in your web browser



## 📦 Dependencies

The app only needs these minimal dependencies:
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `sqlalchemy` - Database ORM
- `httpx` - HTTP client for API calls
- `pydantic` - Data validation
- `python-multipart` - Form data handling

## 🏗️ Project Structure

```
weather-app/
├── backend/
│   ├── main.py              # FastAPI application entry point
│   ├── db.py                # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── crud.py              # Database operations
│   ├── services_open_meteo.py # Weather API service
│   ├── routers/
│   │   ├── weather.py       # Weather endpoints
│   │   └── records.py       # Records endpoints
│   └── requirements.txt     # Python dependencies
├── frontend/
│   └── index.html           # Frontend interface
├── weather.db               # SQLite database
├── setup.py                 # Setup script
└── README.md               # This file
```

## 🌐 API Endpoints

- `GET /health` - Health check
- `GET /api/weather/current-forecast` - Get current weather and 5-day forecast
- `GET /api/records` - Get saved weather records
- `POST /api/records` - Save a weather record

## 🔧 Troubleshooting


### Port Already in Use
If port 8000 is busy, the app will automatically find an available port.

### Database
The app uses SQLite, so no additional database setup is required. The database file (`weather.db`) will be created automatically.

## 📝 Notes

- The app uses the free Open-Meteo API for weather data
- No API keys required
- Data is stored locally in SQLite
- CORS is enabled for local development
