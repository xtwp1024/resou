import json
import sys
import os
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8')

from app.database import SessionLocal
from app.models.models import Star, WeiboData, DouyinData

def parse_fans_count(value):
    if not value:
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        value = value.replace(",", "").replace("+", "").strip()
        if "亿" in value:
            num = float(value.replace("亿", ""))
            return int(num * 100000000)
        elif "万" in value:
            num = float(value.replace("万", ""))
            return int(num * 10000)
        else:
            try:
                return int(value)
            except:
                return None
    return None

def import_stars():
    with open("discovered_stars_9.json", "r", encoding="utf-8") as f:
        stars = json.load(f)
    
    db = SessionLocal()
    added = 0
    skipped = 0
    
    try:
        for star_info in stars:
            name = star_info.get("name")
            if not name:
                continue
            
            existing = db.query(Star).filter(Star.name == name).first()
            if existing:
                skipped += 1
                continue
            
            star = Star(
                name=name,
                category=star_info.get("category", "其他"),
                level=star_info.get("level", "三线"),
                description=star_info.get("description", "")
            )
            db.add(star)
            db.flush()
            
            weibo_fans = parse_fans_count(star_info.get("weibo_fans"))
            if weibo_fans:
                weibo = WeiboData(
                    star_id=star.id,
                    weibo_name=name,
                    fans_count=weibo_fans,
                    verified=True,
                    collect_date=date.today()
                )
                db.add(weibo)
            
            douyin_fans = parse_fans_count(star_info.get("douyin_fans"))
            if douyin_fans:
                douyin = DouyinData(
                    star_id=star.id,
                    douyin_name=name,
                    fans_count=douyin_fans,
                    verified=True,
                    collect_date=date.today()
                )
                db.add(douyin)
            
            added += 1
            print(f"添加: {name} ({star_info.get('level')}, {star_info.get('category')})")
        
        db.commit()
        print(f"\n导入完成: 新增 {added} 个, 跳过 {skipped} 个(已存在)")
    
    except Exception as e:
        db.rollback()
        print(f"错误: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    import_stars()
