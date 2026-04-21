import sys
sys.path.insert(0, '.')
from datetime import date
from app.database import SessionLocal, engine, Base
from app.models.models import Star, WeiboData, DouyinData, XiaohongshuData

Base.metadata.create_all(bind=engine)

STARS_DATA = [
    {"name": "赵丽颖", "gender": "女", "category": "演员", "level": "顶流"},
    {"name": "杨幂", "gender": "女", "category": "演员", "level": "顶流"},
    {"name": "迪丽热巴", "gender": "女", "category": "演员", "level": "顶流"},
    {"name": "杨紫", "gender": "女", "category": "演员", "level": "顶流"},
    {"name": "刘亦菲", "gender": "女", "category": "演员", "level": "顶流"},
    {"name": "杨颖", "gender": "女", "category": "演员", "level": "顶流"},
    {"name": "唐嫣", "gender": "女", "category": "演员", "level": "一线"},
    {"name": "刘诗诗", "gender": "女", "category": "演员", "level": "一线"},
    {"name": "倪妮", "gender": "女", "category": "演员", "level": "一线"},
    {"name": "白鹿", "gender": "女", "category": "演员", "level": "一线"},
    {"name": "赵露思", "gender": "女", "category": "演员", "level": "一线"},
    {"name": "虞书欣", "gender": "女", "category": "演员", "level": "一线"},
    {"name": "王鹤棣", "gender": "男", "category": "演员", "level": "顶流"},
    {"name": "肖战", "gender": "男", "category": "演员", "level": "顶流"},
    {"name": "王一博", "gender": "男", "category": "演员", "level": "顶流"},
    {"name": "易烊千玺", "gender": "男", "category": "演员", "level": "顶流"},
    {"name": "李现", "gender": "男", "category": "演员", "level": "一线"},
    {"name": "杨洋", "gender": "男", "category": "演员", "level": "顶流"},
    {"name": "成毅", "gender": "男", "category": "演员", "level": "一线"},
    {"name": "龚俊", "gender": "男", "category": "演员", "level": "一线"},
    {"name": "胡歌", "gender": "男", "category": "演员", "level": "一线"},
    {"name": "周杰伦", "gender": "男", "category": "歌手", "level": "顶流"},
    {"name": "林俊杰", "gender": "男", "category": "歌手", "level": "顶流"},
    {"name": "薛之谦", "gender": "男", "category": "歌手", "level": "顶流"},
    {"name": "华晨宇", "gender": "男", "category": "歌手", "level": "一线"},
    {"name": "毛不易", "gender": "男", "category": "歌手", "level": "一线"},
    {"name": "蔡徐坤", "gender": "男", "category": "歌手", "level": "顶流"},
    {"name": "鹿晗", "gender": "男", "category": "歌手", "level": "顶流"},
    {"name": "张艺兴", "gender": "男", "category": "歌手", "level": "顶流"},
    {"name": "王俊凯", "gender": "男", "category": "歌手", "level": "顶流"},
    {"name": "王源", "gender": "男", "category": "歌手", "level": "顶流"},
    {"name": "何炅", "gender": "男", "category": "主持人", "level": "顶流"},
    {"name": "谢娜", "gender": "女", "category": "主持人", "level": "顶流"},
    {"name": "汪涵", "gender": "男", "category": "主持人", "level": "顶流"},
    {"name": "李佳琦", "gender": "男", "category": "其他", "level": "顶流"},
    {"name": "薇娅", "gender": "女", "category": "其他", "level": "顶流"},
    {"name": "罗永浩", "gender": "男", "category": "其他", "level": "顶流"},
    {"name": "董宇辉", "gender": "男", "category": "其他", "level": "顶流"},
    {"name": "李子柒", "gender": "女", "category": "其他", "level": "顶流"},
    {"name": "张大仙", "gender": "男", "category": "其他", "level": "顶流"},
    {"name": "马龙", "gender": "男", "category": "其他", "level": "顶流"},
    {"name": "孙颖莎", "gender": "女", "category": "其他", "level": "顶流"},
    {"name": "谷爱凌", "gender": "女", "category": "其他", "level": "顶流"},
    {"name": "全红婵", "gender": "女", "category": "其他", "level": "顶流"},
    {"name": "姚明", "gender": "男", "category": "其他", "level": "顶流"},
    {"name": "刘翔", "gender": "男", "category": "其他", "level": "顶流"},
    {"name": "马云", "gender": "男", "category": "其他", "level": "顶流"},
    {"name": "雷军", "gender": "男", "category": "其他", "level": "顶流"},
    {"name": "撒贝宁", "gender": "男", "category": "其他", "level": "顶流"},
    {"name": "董卿", "gender": "女", "category": "其他", "level": "顶流"},
]

KNOWN_DATA = {
    "赵丽颖": {"weibo_fans": 92320000, "douyin_fans": 32830000},
    "杨幂": {"weibo_fans": 112000000, "douyin_fans": 32000000},
    "迪丽热巴": {"weibo_fans": 82000000, "douyin_fans": 35000000},
    "杨紫": {"weibo_fans": 63000000, "douyin_fans": 28000000},
    "刘亦菲": {"weibo_fans": 71000000, "douyin_fans": 0},
    "杨颖": {"weibo_fans": 105000000, "douyin_fans": 0},
    "唐嫣": {"weibo_fans": 78000000, "douyin_fans": 0},
    "刘诗诗": {"weibo_fans": 72000000, "douyin_fans": 0},
    "倪妮": {"weibo_fans": 48000000, "douyin_fans": 0},
    "白鹿": {"weibo_fans": 25000000, "douyin_fans": 8000000},
    "赵露思": {"weibo_fans": 28000000, "douyin_fans": 15000000},
    "虞书欣": {"weibo_fans": 22000000, "douyin_fans": 12000000},
    "王鹤棣": {"weibo_fans": 20000000, "douyin_fans": 10000000},
    "肖战": {"weibo_fans": 32000000, "douyin_fans": 0},
    "王一博": {"weibo_fans": 40000000, "douyin_fans": 0},
    "易烊千玺": {"weibo_fans": 90000000, "douyin_fans": 0},
    "李现": {"weibo_fans": 24000000, "douyin_fans": 8000000},
    "杨洋": {"weibo_fans": 58000000, "douyin_fans": 15000000},
    "成毅": {"weibo_fans": 26000000, "douyin_fans": 7000000},
    "龚俊": {"weibo_fans": 23000000, "douyin_fans": 6000000},
    "胡歌": {"weibo_fans": 72320000, "douyin_fans": 1016000},
    "周杰伦": {"weibo_fans": 83000000, "douyin_fans": 0},
    "林俊杰": {"weibo_fans": 62000000, "douyin_fans": 0},
    "薛之谦": {"weibo_fans": 57000000, "douyin_fans": 45000000},
    "华晨宇": {"weibo_fans": 42000000, "douyin_fans": 0},
    "毛不易": {"weibo_fans": 28000000, "douyin_fans": 8000000},
    "蔡徐坤": {"weibo_fans": 38000000, "douyin_fans": 0},
    "鹿晗": {"weibo_fans": 63000000, "douyin_fans": 0},
    "张艺兴": {"weibo_fans": 53000000, "douyin_fans": 0},
    "王俊凯": {"weibo_fans": 83000000, "douyin_fans": 0},
    "王源": {"weibo_fans": 85000000, "douyin_fans": 0},
    "何炅": {"weibo_fans": 125000000, "douyin_fans": 0},
    "谢娜": {"weibo_fans": 128000000, "douyin_fans": 0},
    "汪涵": {"weibo_fans": 52000000, "douyin_fans": 0},
    "李佳琦": {"weibo_fans": 35000000, "douyin_fans": 45000000},
    "薇娅": {"weibo_fans": 28000000, "douyin_fans": 0},
    "罗永浩": {"weibo_fans": 15000000, "douyin_fans": 18000000},
    "董宇辉": {"weibo_fans": 12000000, "douyin_fans": 25000000},
    "李子柒": {"weibo_fans": 25000000, "douyin_fans": 55000000},
    "张大仙": {"weibo_fans": 8000000, "douyin_fans": 55000000},
    "马龙": {"weibo_fans": 8000000, "douyin_fans": 5000000},
    "孙颖莎": {"weibo_fans": 5000000, "douyin_fans": 3000000},
    "谷爱凌": {"weibo_fans": 6500000, "douyin_fans": 8000000},
    "全红婵": {"weibo_fans": 3000000, "douyin_fans": 2000000},
    "姚明": {"weibo_fans": 0, "douyin_fans": 0},
    "刘翔": {"weibo_fans": 25000000, "douyin_fans": 0},
    "马云": {"weibo_fans": 25000000, "douyin_fans": 0},
    "雷军": {"weibo_fans": 22000000, "douyin_fans": 30000000},
    "撒贝宁": {"weibo_fans": 0, "douyin_fans": 0},
    "董卿": {"weibo_fans": 0, "douyin_fans": 0},
}

db = SessionLocal()

try:
    print("=" * 60)
    print("开始导入明星数据...")
    print("=" * 60)
    
    added_count = 0
    
    for star_data in STARS_DATA:
        star = Star(**star_data)
        db.add(star)
        db.flush()
        
        if star_data["name"] in KNOWN_DATA:
            data = KNOWN_DATA[star_data["name"]]
            
            if data.get("weibo_fans", 0) > 0:
                weibo = WeiboData(
                    star_id=star.id,
                    weibo_name=star_data["name"],
                    fans_count=data["weibo_fans"],
                    verified=True,
                    collect_date=date.today()
                )
                db.add(weibo)
            
            if data.get("douyin_fans", 0) > 0:
                douyin = DouyinData(
                    star_id=star.id,
                    douyin_name=star_data["name"],
                    fans_count=data["douyin_fans"],
                    verified=True,
                    collect_date=date.today()
                )
                db.add(douyin)
        
        added_count += 1
        print(f"✓ 已添加: {star_data['name']}")
    
    db.commit()
    
    print("=" * 60)
    print(f"导入完成! 共添加 {added_count} 位明星")
    print("=" * 60)
    
    total_stars = db.query(Star).count()
    total_weibo = db.query(WeiboData).count()
    total_douyin = db.query(DouyinData).count()
    
    print(f"\n数据库统计:")
    print(f"明星总数: {total_stars}")
    print(f"微博数据: {total_weibo} 条")
    print(f"抖音数据: {total_douyin} 条")

finally:
    db.close()
