import sys
sys.path.insert(0, '.')
from app.database import SessionLocal
from app.models.models import Star

db = SessionLocal()

total = db.query(Star).count()
print(f"Total: {total}")

categories = db.query(Star.category).distinct().all()
for cat in categories:
    if cat[0]:
        count = db.query(Star).filter(Star.category == cat[0]).count()
        print(f"{cat[0]}: {count}")

levels = db.query(Star.level).distinct().all()
for level in levels:
    if level[0]:
        count = db.query(Star).filter(Star.level == level[0]).count()
        print(f"{level[0]}: {count}")

db.close()
