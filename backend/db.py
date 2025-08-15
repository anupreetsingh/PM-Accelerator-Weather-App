# Anupreet Singh, anupreet2226579@gmail.com
# Role: Database Configuration and Session Management

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Database URL is going to be SQLite file named weather.db in the current directory
DATABASE_URL = "sqlite:///./weather.db" 

# create_engine is a function form SQL Alchemy that sets up a sort of "database dialer" 
# It prepares all the setting so SQL Alchemy know how to connect, what database type to use and what options to apply when you app needs to talk to the database
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)


SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base() # SQL Alchemy registers it tables/columns/relationships in Base.metadata

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
