from datetime import datetime, timezone
print("UTC now:", datetime.now(timezone.utc))
print("Local now:", datetime.now())
