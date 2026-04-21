import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8')

from app.database import SessionLocal
from app.models.models import Star, WeiboData, DouyinData, XiaohongshuData
from sqlalchemy import func

db = SessionLocal()

total_stars = db.query(Star).count()
weibo_count = db.query(WeiboData).count()
douyin_count = db.query(DouyinData).count()
xiaohongshu_count = db.query(XiaohongshuData).count()

print(f"明星总数: {total_stars}")
print(f"微博数据: {weibo_count} 条 (覆盖率: {weibo_count/total_stars*100:.1f}%)")
print(f"抖音数据: {douyin_count} 条 (覆盖率: {douyin_count/total_stars*100:.1f}%)")
print(f"小红书数据: {xiaohongshu_count} 条 (覆盖率: {xiaohongshu_count/total_stars*100:.1f}%)")

stars_without_weibo = db.query(Star).filter(~Star.weibo_data.any()).count()
stars_without_douyin = db.query(Star).filter(~Star.douyin_data.any()).count()
stars_without_xiaohongshu = db.query(Star).filter(~Star.xiaohongshu_data.any()).count()

print(f"\n缺少微博数据: {stars_without_weibo} 个明星")
print(f"缺少抖音数据: {stars_without_douyin} 个明星")
print(f"缺少小红书数据: {stars_without_xiaohongshu} 个明星")

db.close()
