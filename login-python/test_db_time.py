import asyncio
from app.db import SessionLocal
from app.models import User

def check_time():
    db = SessionLocal()
    user = db.query(User).filter(User.username == "ivargasm").first()
    if user:
        print(f"User created_at in DB: {user.created_at}")
        print(f"repr: {repr(user.created_at)}")
    else:
        print("User not found")
    db.close()

check_time()
