import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

db_url = os.getenv("DATABASE_URL")

if not db_url:
    raise ValueError(
        "DATABASE_URL is not set.\n"
        "Create a .env file in this directory based on .env.example.\n"
        "Example: DATABASE_URL=mysql+pymysql://root:password@localhost:3306/expense_tracker_db"
    )

connect_args = {}
if db_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(db_url, echo=False, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
