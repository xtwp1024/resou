from datetime import datetime, date
from typing import Optional
from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Star, WeiboData, DouyinData, XiaohongshuData
from app.schemas.schemas import CrawlResult
from app.crawlers.simple_crawler import WeiboCrawler, DouyinCrawler, XiaohongshuCrawler
import asyncio
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')
os.environ['PYTHONIOENCODING'] = 'utf-8'

router = APIRouter(prefix="/api/crawl", tags=["数据采集"])

crawl_status = {
    "is_running": False,
    "last_run": None,
    "total": 0,
    "current": 0,
    "errors": []
}


async def crawl_weibo_playwright(star_name: str, headless: bool = True):
    from playwright.async_api import async_playwright
    
    results = []
    
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=headless,
                args=['--disable-blink-features=AutomationControlled']
            )
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
            page = await context.new_page()
            
            search_url = f"https://s.weibo.com/user?q={star_name}&Refer=weibo_user"
            await page.goto(search_url, wait_until='networkidle', timeout=30000)
            await asyncio.sleep(2)
            
            user_cards = await page.query_selector_all('.card-user-b')
            
            for card in user_cards[:5]:
                try:
                    name_elem = await card.query_selector('.name')
                    fans_elem = await card.query_selector('.s-nobr')
                    
                    if name_elem:
                        name = await name_elem.inner_text()
                        fans_text = "0"
                        if fans_elem:
                            fans_text = await fans_elem.inner_text()
                            if '粉丝：' in fans_text:
                                fans_text = fans_text.replace('粉丝：', '')
                        
                        fans_count = parse_fans_count(fans_text)
                        
                        results.append({
                            "weibo_name": name.strip(),
                            "fans_count": fans_count,
                            "collect_date": str(date.today())
                        })
                except:
                    pass
            
            await browser.close()
    except Exception as e:
        print(f"Playwright 微博爬虫错误: {e}")
    
    return results


def parse_fans_count(text: str) -> int:
    text = text.strip().replace(',', '')
    if '万' in text:
        num = float(text.replace('万', '').strip())
        return int(num * 10000)
    elif '亿' in text:
        num = float(text.replace('亿', '').strip())
        return int(num * 100000000)
    else:
        try:
            return int(text.replace(',', '').strip())
        except:
            return 0

async def crawl_star_data(star_id: int, db: Session):
    star = db.query(Star).filter(Star.id == star_id).first()
    if not star:
        return None
    
    results = {}
    
    weibo_crawler = WeiboCrawler()
    douyin_crawler = DouyinCrawler()
    xiaohongshu_crawler = XiaohongshuCrawler()
    
    try:
        weibo_users = await weibo_crawler.search_user(star.name)
        if weibo_users:
            best_match = weibo_users[0]
            weibo_data = WeiboData(
                star_id=star_id,
                weibo_id=best_match.get('weibo_id'),
                weibo_name=best_match.get('weibo_name'),
                fans_count=best_match.get('fans_count', 0),
                verified=best_match.get('verified', False),
                avatar=best_match.get('avatar')
            )
            db.add(weibo_data)
            results['weibo'] = best_match
    except Exception as e:
        results['weibo_error'] = str(e)
    
    try:
        douyin_users = await douyin_crawler.search_user(star.name)
        if douyin_users:
            best_match = douyin_users[0]
            douyin_data = DouyinData(
                star_id=star_id,
                douyin_id=best_match.get('douyin_id'),
                douyin_name=best_match.get('douyin_name'),
                fans_count=best_match.get('fans_count', 0),
                verified=best_match.get('verified', False),
                avatar=best_match.get('avatar')
            )
            db.add(douyin_data)
            results['douyin'] = best_match
    except Exception as e:
        results['douyin_error'] = str(e)
    
    try:
        xiaohongshu_users = await xiaohongshu_crawler.search_user(star.name)
        if xiaohongshu_users:
            best_match = xiaohongshu_users[0]
            xiaohongshu_data = XiaohongshuData(
                star_id=star_id,
                xhs_id=best_match.get('xhs_id'),
                xhs_name=best_match.get('xhs_name'),
                fans_count=best_match.get('fans_count', 0),
                likes_collects_count=best_match.get('likes_collects_count', 0),
                verified=best_match.get('verified', False),
                has_official_account=best_match.get('verified', False),
                avatar=best_match.get('avatar')
            )
            db.add(xiaohongshu_data)
            results['xiaohongshu'] = best_match
    except Exception as e:
        results['xiaohongshu_error'] = str(e)
    
    db.commit()
    return results

@router.post("/weibo/{star_id}", response_model=CrawlResult)
async def crawl_weibo(star_id: int, db: Session = Depends(get_db)):
    star = db.query(Star).filter(Star.id == star_id).first()
    if not star:
        return CrawlResult(success=False, message="明星不存在")
    
    try:
        users = await crawl_weibo_playwright(star.name, headless=True)
        if users:
            best_match = users[0]
            weibo_data = WeiboData(
                star_id=star_id,
                weibo_name=best_match.get('weibo_name'),
                fans_count=best_match.get('fans_count', 0),
                verified=best_match.get('verified', False),
                collect_date=date.today()
            )
            db.add(weibo_data)
            db.commit()
            return CrawlResult(success=True, message="采集成功", data=best_match)
        return CrawlResult(success=False, message="未找到用户")
    except Exception as e:
        return CrawlResult(success=False, message=f"采集失败: {str(e)}")

@router.post("/douyin/{star_id}", response_model=CrawlResult)
async def crawl_douyin(star_id: int, db: Session = Depends(get_db)):
    star = db.query(Star).filter(Star.id == star_id).first()
    if not star:
        return CrawlResult(success=False, message="明星不存在")
    
    crawler = DouyinCrawler()
    try:
        users = await crawler.search_user(star.name)
        if users:
            best_match = users[0]
            douyin_data = DouyinData(
                star_id=star_id,
                douyin_id=best_match.get('douyin_id'),
                douyin_name=best_match.get('douyin_name'),
                fans_count=best_match.get('fans_count', 0),
                verified=best_match.get('verified', False),
                avatar=best_match.get('avatar')
            )
            db.add(douyin_data)
            db.commit()
            return CrawlResult(success=True, message="采集成功", data=best_match)
        return CrawlResult(success=False, message="未找到用户")
    except Exception as e:
        return CrawlResult(success=False, message=f"采集失败: {str(e)}")

@router.post("/xiaohongshu/{star_id}", response_model=CrawlResult)
async def crawl_xiaohongshu(star_id: int, db: Session = Depends(get_db)):
    star = db.query(Star).filter(Star.id == star_id).first()
    if not star:
        return CrawlResult(success=False, message="明星不存在")
    
    crawler = XiaohongshuCrawler()
    try:
        users = await crawler.search_user(star.name)
        if users:
            best_match = users[0]
            xiaohongshu_data = XiaohongshuData(
                star_id=star_id,
                xhs_id=best_match.get('xhs_id'),
                xhs_name=best_match.get('xhs_name'),
                fans_count=best_match.get('fans_count', 0),
                likes_collects_count=best_match.get('likes_collects_count', 0),
                verified=best_match.get('verified', False),
                has_official_account=best_match.get('verified', False),
                avatar=best_match.get('avatar')
            )
            db.add(xiaohongshu_data)
            db.commit()
            return CrawlResult(success=True, message="采集成功", data=best_match)
        return CrawlResult(success=False, message="未找到用户")
    except Exception as e:
        return CrawlResult(success=False, message=f"采集失败: {str(e)}")

@router.post("/all")
async def crawl_all(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    global crawl_status
    
    if crawl_status["is_running"]:
        return {"message": "采集任务正在进行中", "status": crawl_status}
    
    stars = db.query(Star).all()
    crawl_status = {
        "is_running": True,
        "last_run": datetime.now(),
        "total": len(stars),
        "current": 0,
        "errors": []
    }
    
    async def run_crawl():
        global crawl_status
        for star in stars:
            try:
                await crawl_star_data(star.id, db)
                crawl_status["current"] += 1
            except Exception as e:
                crawl_status["errors"].append(f"{star.name}: {str(e)}")
        crawl_status["is_running"] = False
    
    background_tasks.add_task(run_crawl)
    
    return {"message": "采集任务已启动", "total": len(stars)}

@router.get("/status")
def get_crawl_status():
    return crawl_status
