import time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError

from app.core.config import settings


DATABASE_URL = settings.DATABASE_URL

MAX_RETRIES = 10
RETRY_DELAY = 3


for attempt in range(MAX_RETRIES):

    try:
        engine = create_engine(DATABASE_URL)

        connection = engine.connect()

        connection.close()

        print("Database connection successful!")

        break

    except OperationalError:

        print(
            f"Database unavailable. Retrying in {RETRY_DELAY} seconds..."
        )

        time.sleep(RETRY_DELAY)

else:
    raise Exception("Could not connect to PostgreSQL")


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()