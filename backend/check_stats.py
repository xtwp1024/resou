import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8')

from app.database import SessionLocal
from app.models.models import Star, WeiboData, DouyinData
from sqlalchemy import func

db = SessionLocal()

total_stars = db.query(Star).count()
print(f"数据库中明星总数: {total_stars}")

level_counts = db.query(Star.level, func.count(Star.id)).group_by(Star.level).all()
print("\n按等级统计:")
for level, count in level_counts:
    print(f"  {level}: {count}")

category_counts = db.query(Star.category, func.count(Star.id)).group_by(Star.category).all()
print("\n按类型统计:")
for category, count in category_counts:
    print(f"  {category}: {count}")

weibo_count = db.query(WeiboData).count()
douyin_count = db.query(DouyinData).count()
print(f"\n微博数据: {weibo_count} 条")
print(f"抖音数据: {douyin_count} 条")

db.close()
