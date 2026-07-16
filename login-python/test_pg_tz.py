from app.db import SessionLocal
from sqlalchemy import text
db = SessionLocal()
result = db.execute(text("SHOW TIMEZONE;")).scalar()
print("Postgres TimeZone:", result)
db.close()
