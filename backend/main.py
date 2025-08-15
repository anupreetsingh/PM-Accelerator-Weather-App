# Anupreet Singh, anupreet2226579@gmail.com
# Role: FastAPI Application Entry Point and Server Configuration

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import Base, engine
from .routers import weather, records

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Weather App") # Instance of FastAPI, going to be entry point to our backend

# Allow local file to call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

# Inclluding the Router files in main Backend
app.include_router(weather.router) # From the "weather" file include the APIRouter instance named "router"
app.include_router(records.router)# From the "records" file include the APIRouter instance named "router"

@app.get("/health")
def health():
    return {"ok": True}

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
