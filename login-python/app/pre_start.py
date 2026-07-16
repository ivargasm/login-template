import logging
from sqlalchemy import create_engine, text
from app.config import DATABASE_URL, SCHEMA

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_schema() -> None:
    try:
        # Create a raw connection engine without pooling to just create the schema
        engine = create_engine(DATABASE_URL)
        with engine.connect() as connection:
            if SCHEMA and SCHEMA != "public":
                # Create schema if it doesn't exist
                logger.info(f"Checking/creating schema: {SCHEMA}")
                connection.execute(text(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA}"))
                connection.commit()
                logger.info("Schema is ready.")
            else:
                logger.info("Using default 'public' schema.")
    except Exception as e:
        logger.error(f"Error checking/creating schema: {e}")
        raise e

if __name__ == "__main__":
    create_schema()
