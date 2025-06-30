from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load variables from .env into the system environment
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Create engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # show SQL logs
)

# Create async session
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)
