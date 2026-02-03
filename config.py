import os
from dotenv import load_dotenv

# Load environment variables from a .env file if it exists
load_dotenv()

# Database Configuration
# Defaults are set for the local Docker Compose environment
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "admin123")
DB_HOST = os.getenv("DB_HOST", "localhost") # Changed default to localhost for local run, Docker overrides it
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "river_plate_db")

def get_db_url():
    """Returns the SQLAlchemy database URL constructed from environment variables."""
    # Handle potential differnces in driver names if needed, but postgresql is standard
    return f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
