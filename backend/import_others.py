import sys
sys.path.insert(0, '.')
from datetime import date
from app.database import SessionLocal
from app.models.models import Star, WeiboData, DouyinData, XiaohongshuData

OTHER_HIGH_PROFILE = [
    {"name": "李佳琦", "gender": "男", "category": "其他", "level": "顶流"},
    {"name": "薇娅", "gender": "女", "category": "其他", "level": "顶流"},
    {"name": "罗永浩", "gender": "男", "category": "其他", "level": "顶流"},
    {"name": "董宇辉", "gender": "男", "category": "其他", "level": "顶流"},
    {"name": "李子柒", "gender": "女", "category": "其他", "level": "顶流"},
    {"name": "papi酱", "gender": "女", "category": "其他", "level": "一线"},
    {"name": "冯提莫", "gender": "女", "category": "其他", "level": "一线"},
    {"name": "张大仙", "gender": "男", "category": "其他", "level": "顶流"},
    {"name": "旭旭宝宝", "gender": "男", "category": "其他", "level": "一线"},
    {"name": "PDD", "gender": "男", "category": "其他", "level": "一线"},
    {"name": "大司马", "gender": "男", "category": "其他", "level": "一线"},
    {"name": "周淑怡", "gender": "女", "category": "其他", "level": "二线"},
    {"name": "小团团", "gender": "女", "category": "其他", "level": "一线"},
    {"name": "Uzi", "gender": "男", "category": "其他", "level": "顶流"},
    {"name": "TheShy", "gender": "男", "category": "其他", "level": "一线"},
    {"name": "Faker", "gender": "男", "category": "其他", "level": "顶流"},
    {"name": "马龙", "gender": "男", "category": "其他", "level": "顶流"},
    {"name": "樊振东", "gender": "男", "category": "其他", "level": "顶流"},
    {"name": "孙颖莎", "gender": "女", "category": "其他", "level": "顶流"},
    {"name": "陈梦", "gender": "女", "category": "其他", "level": "一线"},
    {"name": "王楚钦", "gender": "男", "category": "其他", "level": "一线"},
    {"name": "张继科", "gender": "男", "category": "其他", "level": "顶流"},
    {"name": "刘国梁", "gender": "男", "category": "其他", "level": "一线"},
    {"name": "姚明", "gender": "男", "category": "其他", "level": "顶流"},
    {"name": "易建联", "gender": "男", "category": "其他", "level": "顶流"},
    {"name": "郭艾伦", "gender": "男", "category": "其他", "level": "一线"},
    {"name": "林书豪", "gender": "男", "category": "其他", "level": "一线"},
    {"name": "苏炳添", "gender": "男", "category": "其他", "level": "顶流"},
    {"name": "谷爱凌", "gender": "女", "category": "其他", "level": "顶流"},
    {"name": "武大靖", "gender": "男", "category": "其他", "level": "一线"},
    {"name": "全红婵", "gender": "女", "category": "其他", "level": "顶流"},
    {"name": "郭晶晶", "gender": "女", "category": "其他", "level": "顶流"},
    {"name": "田亮", "gender": "男", "category": "其他", "level": "一线"},
    {"name": "刘翔", "gender": "男", "category": "其他", "level": "顶流"},
    {"name": "郎平", "gender": "女", "category": "其他", "level": "顶流"},
    {"name": "朱婷", "gender": "女", "category": "其他", "level": "一线"},
    {"name": "惠若琪", "gender": "女", "category": "其他", "level": "一线"},
    {"name": "张常宁", "gender": "女", "category": "其他", "level": "一线"},
    {"name": "李宁", "gender": "男", "category": "其他", "level": "顶流"},
    {"name": "李小鹏", "gender": "男", "category": "其他", "level": "一线"},
    {"name": "杨威", "gender": "男", "category": "其他", "level": "一线"},
    {"name": "邹凯", "gender": "男", "category": "其他", "level": "二线"},
    {"name": "马云", "gender": "男", "category": "其他", "level": "顶流"},
    {"name": "马化腾", "gender": "男", "category": "其他", "level": "顶流"},
    {"name": "雷军", "gender": "男", "category": "其他", "level": "顶流"},
    {"name": "刘强东", "gender": "男", "category": "其他", "level": "顶流"},
    {"name": "王健林", "gender": "男", "category": "其他", "level": "顶流"},
    {"name": "董明珠", "gender": "女", "category": "其他", "level": "顶流"},
    {"name": "俞敏洪", "gender": "男", "category": "其他", "level": "一线"},
    {"name": "张一鸣", "gender": "男", "category": "其他", "level": "顶流"},
    {"name": "黄峥", "gender": "男", "category": "其他", "level": "顶流"},
    {"name": "王兴", "gender": "男", "category": "其他", "level": "一线"},
    {"name": "李彦宏", "gender": "男", "category": "其他", "level": "顶流"},
    {"name": "丁磊", "gender": "男", "category": "其他", "level": "一线"},
    {"name": "周鸿祎", "gender": "男", "category": "其他", "level": "一线"},
    {"name": "王小川", "gender": "男", "category": "其他", "level": "二线"},
    {"name": "宿华", "gender": "男", "category": "其他", "level": "二线"},
    {"name": "程一笑", "gender": "男", "category": "其他", "level": "二线"},
    {"name": "陈欧", "gender": "男", "category": "其他", "level": "三线"},
    {"name": "罗振宇", "gender": "男", "category": "其他", "level": "一线"},
    {"name": "吴晓波", "gender": "男", "category": "其他", "level": "一线"},
    {"name": "樊登", "gender": "男", "category": "其他", "level": "一线"},
    {"name": "刘润", "gender": "男", "category": "其他", "level": "二线"},
    {"name": "张泉灵", "gender": "女", "category": "其他", "level": "一线"},
    {"name": "杨澜", "gender": "女", "category": "其他", "level": "顶流"},
    {"name": "鲁豫", "gender": "女", "category": "其他", "level": "一线"},
    {"name": "董卿", "gender": "女", "category": "其他", "level": "顶流"},
    {"name": "周涛", "gender": "女", "category": "其他", "level": "一线"},
    {"name": "朱军", "gender": "男", "category": "其他", "level": "一线"},
    {"name": "撒贝宁", "gender": "男", "category": "其他", "level": "顶流"},
    {"name": "康辉", "gender": "男", "category": "其他", "level": "一线"},
    {"name": "白岩松", "gender": "男", "category": "其他", "level": "一线"},
    {"name": "水均益", "gender": "男", "category": "其他", "level": "二线"},
    {"name": "敬一丹", "gender": "女", "category": "其他", "level": "二线"},
    {"name": "李咏", "gender": "男", "category": "其他", "level": "顶流"},
    {"name": "华少", "gender": "男", "category": "其他", "level": "一线"},
    {"name": "汪涵", "gender": "男", "category": "其他", "level": "顶流"},
]

KNOWN_DATA = {
    "李佳琦": {"weibo_fans": 35000000, "douyin_fans": 45000000},
    "薇娅": {"weibo_fans": 28000000, "douyin_fans": 0},
    "罗永浩": {"weibo_fans": 15000000, "douyin_fans": 18000000},
    "董宇辉": {"weibo_fans": 12000000, "douyin_fans": 25000000},
    "李子柒": {"weibo_fans": 25000000, "douyin_fans": 55000000},
    "papi酱": {"weibo_fans": 32000000, "douyin_fans": 35000000},
    "张大仙": {"weibo_fans": 8000000, "douyin_fans": 55000000},
    "Uzi": {"weibo_fans": 8000000, "douyin_fans": 10000000},
    "马龙": {"weibo_fans": 8000000, "douyin_fans": 5000000},
    "孙颖莎": {"weibo_fans": 5000000, "douyin_fans": 3000000},
    "谷爱凌": {"weibo_fans": 6500000, "douyin_fans": 8000000},
    "全红婵": {"weibo_fans": 3000000, "douyin_fans": 2000000},
    "姚明": {"weibo_fans": 0, "douyin_fans": 0},
    "刘翔": {"weibo_fans": 25000000, "douyin_fans": 0},
    "马云": {"weibo_fans": 25000000, "douyin_fans": 0},
    "雷军": {"weibo_fans": 22000000, "douyin_fans": 30000000},
    "董明珠": {"weibo_fans": 500000, "douyin_fans": 800000},
    "撒贝宁": {"weibo_fans": 0, "douyin_fans": 0},
    "董卿": {"weibo_fans": 0, "douyin_fans": 0},
    "杨澜": {"weibo_fans": 45000000, "douyin_fans": 0},
    "汪涵": {"weibo_fans": 52000000, "douyin_fans": 0},
}

db = SessionLocal()

try:
    print("=" * 60)
    print("开始批量导入其他类别高粉丝人员...")
    print("=" * 60)
    
    added_count = 0
    skipped_count = 0
    
    for star_data in OTHER_HIGH_PROFILE:
        existing = db.query(Star).filter(Star.name == star_data["name"]).first()
        if existing:
            skipped_count += 1
            continue
        
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
        print(f"✓ 已添加: {star_data['name']} ({star_data['category']})")
    
    db.commit()
    
    print("=" * 60)
    print(f"导入完成!")
    print(f"新增: {added_count} 位")
    print(f"跳过: {skipped_count} 位 (已存在)")
    print("=" * 60)
    
    total_stars = db.query(Star).count()
    total_weibo = db.query(WeiboData).count()
    total_douyin = db.query(DouyinData).count()
    total_xiaohongshu = db.query(XiaohongshuData).count()
    
    print(f"\n数据库统计:")
    print(f"总人数: {total_stars}")
    print(f"微博数据: {total_weibo} 条")
    print(f"抖音数据: {total_douyin} 条")
    print(f"小红书数据: {total_xiaohongshu} 条")
    
    by_category = {}
    categories = db.query(Star.category).distinct().all()
    for cat in categories:
        if cat[0]:
            count = db.query(Star).filter(Star.category == cat[0]).count()
            by_category[cat[0]] = count
    print(f"\n按类型统计:")
    for cat, count in sorted(by_category.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count} 位")

finally:
    db.close()
