from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from app.config import SCHEDULER_CONFIG
from app.database import SessionLocal
from app.models.models import Star
from app.api.crawl import crawl_star_data

scheduler = AsyncIOScheduler()

async def daily_crawl_task():
    db = SessionLocal()
    try:
        stars = db.query(Star).all()
        print(f"[{datetime.now()}] 开始每日数据采集，共 {len(stars)} 位明星")
        
        for i, star in enumerate(stars):
            try:
                await crawl_star_data(star.id, db)
                print(f"[{datetime.now()}] 完成 {star.name} ({i+1}/{len(stars)})")
            except Exception as e:
                print(f"[{datetime.now()}] 采集 {star.name} 失败: {e}")
        
        print(f"[{datetime.now()}] 每日数据采集完成")
    finally:
        db.close()

def setup_scheduler():
    hour = SCHEDULER_CONFIG.get("hour", 2)
    minute = SCHEDULER_CONFIG.get("minute", 0)
    
    scheduler.add_job(
        daily_crawl_task,
        CronTrigger(hour=hour, minute=minute),
        id="daily_crawl",
        name="每日数据采集",
        replace_existing=True
    )
    
    return scheduler

def start_scheduler():
    setup_scheduler()
    scheduler.start()
    print(f"定时任务已启动，将在每日 {SCHEDULER_CONFIG.get('hour', 2):02d}:{SCHEDULER_CONFIG.get('minute', 0):02d} 执行采集")

def stop_scheduler():
    scheduler.shutdown()
    print("定时任务已停止")
