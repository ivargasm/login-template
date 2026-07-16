from app.db import SessionLocal
from app.models import User
from datetime import datetime, timezone
db = SessionLocal()
user = db.query(User).filter(User.username == "ivargasm").first()
if user:
    user.created_at = datetime.now(timezone.utc)
    db.commit()
    print("User updated to current UTC.")
else:
    print("User not found")
db.close()
