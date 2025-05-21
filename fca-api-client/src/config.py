from dotenv import load_dotenv
import os
from sqlalchemy import create_engine

# Load environment variables at the start
load_dotenv()

# Database connection string
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL must be set in the .env file")

def load_config():
    """
    Validate required environment variables.

    This function ensures that critical environment variables are set.
    """
    if not os.getenv("X_AUTH_EMAIL") or not os.getenv("X_AUTH_KEY"):
        raise ValueError("X_AUTH_EMAIL and X_AUTH_KEY must be set in .env")

# Create a SQLAlchemy engine
engine = create_engine(DATABASE_URL)