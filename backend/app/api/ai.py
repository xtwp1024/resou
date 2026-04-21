import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Star, WeiboData, DouyinData, XiaohongshuData
from app.schemas.schemas import StarCreate, StarResponse, CrawlResult
from app.services.minimax_client import MiniMaxClient
from app.config import MINIMAX_CONFIG
from datetime import date
import json

router = APIRouter(prefix="/api/ai", tags=["AI智能"])

MINIMAX_API_KEY = MINIMAX_CONFIG.get("api_key", "")
MINIMAX_GROUP_ID = MINIMAX_CONFIG.get("group_id", "")
MINIMAX_BASE_URL = MINIMAX_CONFIG.get("base_url", "https://api.minimaxi.com/v1/chat/completions")
MINIMAX_MODEL = MINIMAX_CONFIG.get("model", "MiniMax-M2.5")

def get_minimax_client():
    if not MINIMAX_API_KEY:
        raise HTTPException(status_code=500, detail="MINIMAX_API_KEY 未配置")
    return MiniMaxClient(MINIMAX_API_KEY, MINIMAX_GROUP_ID, MINIMAX_BASE_URL, MINIMAX_MODEL)

@router.post("/discover")
async def discover_stars(
    query: str,
    auto_add: bool = True,
    db: Session = Depends(get_db),
    client: MiniMaxClient = Depends(get_minimax_client)
):
    discovered = await client.discover_stars(query)
    
    added_stars = []
    skipped_stars = []
    
    if auto_add:
        for star_info in discovered:
            existing = db.query(Star).filter(Star.name == star_info.get("name")).first()
            if existing:
                skipped_stars.append(star_info.get("name"))
                continue
            
            star = Star(
                name=star_info.get("name"),
                category=star_info.get("category", "其他"),
                level=star_info.get("level", "三线"),
                description=star_info.get("description", "")
            )
            db.add(star)
            db.flush()
            
            weibo_fans = star_info.get("weibo_fans", 0)
            douyin_fans = star_info.get("douyin_fans", 0)
            xiaohongshu_fans = star_info.get("xiaohongshu_fans", 0)
            
            if weibo_fans:
                weibo = WeiboData(
                    star_id=star.id,
                    weibo_name=star_info.get("name"),
                    fans_count=weibo_fans,
                    verified=True,
                    collect_date=date.today()
                )
                db.add(weibo)
            
            if douyin_fans:
                douyin = DouyinData(
                    star_id=star.id,
                    douyin_name=star_info.get("name"),
                    fans_count=douyin_fans,
                    verified=True,
                    collect_date=date.today()
                )
                db.add(douyin)
            
            if xiaohongshu_fans:
                xiaohongshu = XiaohongshuData(
                    star_id=star.id,
                    xhs_name=star_info.get("name"),
                    fans_count=xiaohongshu_fans,
                    verified=True,
                    has_official_account=True,
                    collect_date=date.today()
                )
                db.add(xiaohongshu)
            
            added_stars.append(star_info.get("name"))
        
        db.commit()
    
    return {
        "discovered": len(discovered),
        "added": added_stars,
        "skipped": skipped_stars,
        "stars": discovered
    }

@router.post("/complete/{star_id}")
async def complete_star_data(
    star_id: int,
    db: Session = Depends(get_db),
    client: MiniMaxClient = Depends(get_minimax_client)
):
    star = db.query(Star).filter(Star.id == star_id).first()
    if not star:
        raise HTTPException(status_code=404, detail="明星不存在")
    
    data = await client.complete_star_data(star.name)
    
    if data.get("weibo_fans"):
        existing = db.query(WeiboData).filter(
            WeiboData.star_id == star_id,
            WeiboData.collect_date == date.today()
        ).first()
        if not existing:
            weibo = WeiboData(
                star_id=star_id,
                weibo_name=star.name,
                fans_count=data["weibo_fans"],
                verified=True,
                collect_date=date.today()
            )
            db.add(weibo)
    
    if data.get("douyin_fans"):
        existing = db.query(DouyinData).filter(
            DouyinData.star_id == star_id,
            DouyinData.collect_date == date.today()
        ).first()
        if not existing:
            douyin = DouyinData(
                star_id=star_id,
                douyin_name=star.name,
                fans_count=data["douyin_fans"],
                verified=True,
                collect_date=date.today()
            )
            db.add(douyin)
    
    if data.get("xiaohongshu_fans"):
        existing = db.query(XiaohongshuData).filter(
                XiaohongshuData.star_id == star_id,
                XiaohongshuData.collect_date == date.today()
            ).first()
        if not existing:
            xiaohongshu = XiaohongshuData(
                star_id=star_id,
                xhs_name=star.name,
                fans_count=data["xiaohongshu_fans"],
                verified=True,
                has_official_account=data.get("has_xiaohongshu", False),
                collect_date=date.today()
            )
            db.add(xiaohongshu)
    
    if data.get("category"):
        star.category = data["category"]
    if data.get("level"):
        star.level = data["level"]
    
    db.commit()
    
    return {
        "success": True,
        "message": "数据补全完成",
        "data": data
    }

@router.post("/batch-discover")
async def batch_discover(
    queries: list[str],
    db: Session = Depends(get_db),
    client: MiniMaxClient = Depends(get_minimax_client)
):
    all_discovered = []
    all_added = []
    
    for query in queries:
        discovered = await client.discover_stars(query)
        all_discovered.extend(discovered)
        
        for star_info in discovered:
            existing = db.query(Star).filter(Star.name == star_info.get("name")).first()
            if existing:
                continue
            
            star = Star(
                name=star_info.get("name"),
                category=star_info.get("category", "其他"),
                level=star_info.get("level", "三线"),
                description=star_info.get("description", "")
            )
            db.add(star)
            db.flush()
            
            if star_info.get("weibo_fans"):
                weibo = WeiboData(
                    star_id=star.id,
                    weibo_name=star_info.get("name"),
                    fans_count=star_info.get("weibo_fans", 0),
                    verified=True,
                    collect_date=date.today()
                )
                db.add(weibo)
            
            if star_info.get("douyin_fans"):
                douyin = DouyinData(
                    star_id=star.id,
                    douyin_name=star_info.get("name"),
                    fans_count=star_info.get("douyin_fans", 0),
                    verified=True,
                    collect_date=date.today()
                )
                db.add(douyin)
            
            if star_info.get("xiaohongshu_fans"):
                xiaohongshu = XiaohongshuData(
                    star_id=star.id,
                    xhs_name=star_info.get("name"),
                    fans_count=star_info.get("xiaohongshu_fans", 0),
                    verified=True,
                    has_official_account=True,
                    collect_date=date.today()
                )
                db.add(xiaohongshu)
            
            all_added.append(star_info.get("name"))
    
    db.commit()
    
    return {
        "total_discovered": len(all_discovered),
        "total_added": len(all_added),
        "discovered": all_discovered
    }
