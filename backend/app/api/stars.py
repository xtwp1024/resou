from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from app.database import get_db
from app.models.models import Star, WeiboData, DouyinData, XiaohongshuData
from app.schemas.schemas import (
    StarCreate, StarUpdate, StarResponse, StarListResponse,
    StarDetailResponse, StatsResponse
)

from pydantic import BaseModel
from typing import Optional


import json

router = APIRouter(prefix="/api/stars", tags=["明星管理"])

class FanDataUpdate(BaseModel):
    weibo_fans: Optional[int] = None
    douyin_fans: Optional[int] = None
    xiaohongshu_fans: Optional[int] = None

    weibo_verified: Optional[bool] = None
    douyin_verified: Optional[bool] = None
    xiaohongshu_verified: Optional[bool] = None

    description: Optional[str] = None

@router.get("", response_model=StarListResponse)
def get_stars(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    keyword: Optional[str] = None,
    level: Optional[str] = None,
    category: Optional[str] = None,
    sort_by: str = "updated_at",
    order: str = "desc",
    db: Session = Depends(get_db)
):
    query = db.query(Star)
    
    if keyword:
        query = query.filter(Star.name.contains(keyword) | Star.english_name.contains(keyword))
    if level:
        query = query.filter(Star.level == level)
    if category:
        query = query.filter(Star.category == category)
    
    total = query.count()
    
    if order == "desc":
        query = query.order_by(desc(getattr(Star, sort_by, Star.updated_at)))
    else:
        query = query.order_by(getattr(Star, sort_by, Star.updated_at))
    
    offset = (page - 1) * page_size
    items = query.offset(offset).limit(page_size).all()
    
    result_items = []
    for star in items:
        weibo = db.query(WeiboData).filter(WeiboData.star_id == star.id).order_by(desc(WeiboData.collect_date)).first()
        douyin = db.query(DouyinData).filter(DouyinData.star_id == star.id).order_by(desc(DouyinData.collect_date)).first()
        xiaohongshu = db.query(XiaohongshuData).filter(XiaohongshuData.star_id == star.id).order_by(desc(Xiaohongshu.collect_date)).first()
        
        result_items.append({
            "id": star.id,
            "name": star.name,
            "english_name": star.english_name,
            "gender": star.gender,
            "category": star.category,
            "level": star.level,
            "agency": star.agency,
            "birthday": star.birthday,
            "avatar": star.avatar,
            "created_at": star.created_at,
            "updated_at": star.updated_at,
            "weibo_fans": weibo.fans_count if weibo else None,
            "douyin_fans": douyin.fans_count if douyin else None,
            "xiaohongshu_fans": xiaohongshu.fans_count if xiaohongshu else None,
        })
    
    return {"total": total, "items": result_items}

@router.get("/stats", response_model=StatsResponse)
def get_stats(db: Session = Depends(get_db)):
    total_stars = db.query(Star).count()
    
    by_level = {}
    for level in ["顶流", "一线", "二线", "三线"]:
        count = db.query(Star).filter(Star.level == level).count()
        by_level[level] = count
    
    by_category = {}
    categories = db.query(Star.category).distinct().all()
    for cat in categories:
        if cat[0]:
            count = db.query(Star).filter(Star.category == cat[0]).count()
            by_category[cat[0]] = count
    
    last_crawl = db.query(WeiboData).order_by(desc(WeiboData.created_at)).first()
    last_crawl_time = last_crawl.created_at if last_crawl else None
    
    total_weibo = db.query(WeiboData).count()
    total_douyin = db.query(DouyinData).count()
    total_xiaohongshu = db.query(XiaohongshuData).count()
    
    return {
        "total_stars": total_stars,
        "by_level": by_level,
        "by_category": by_category,
        "last_crawl_time": last_crawl_time,
        "total_weibo": total_weibo,
        "total_douyin": total_douyin,
        "total_xiaohongshu": total_xiaohongshu,
    }

@router.get("/{star_id}", response_model=StarDetailResponse)
def get_star(star_id: int, db: Session = Depends(get_db)):
    star = db.query(Star).filter(Star.id == star_id).first()
    if not star:
        raise HTTPException(status_code=404, detail="明星不存在")
    
    weibo = db.query(WeiboData).filter(WeiboData.star_id == star_id).order_by(desc(WeiboData.collect_date)).first()
    douyin = db.query(DouyinData).filter(DouyinData.star_id == star_id).order_by(desc(DouyinData.collect_date)).first()
    xiaohongshu = db.query(XiaohongshuData).filter(Xiaohongshu.star_id == star_id).order_by(desc(Xiaohongshu.collect_date)).first()
    
    result = StarDetailResponse(
        id=star.id,
        name=star.name,
        english_name=star.english_name,
        gender=star.gender,
        category=star.category,
        level=star.level,
        agency=star.agency,
        birthday=star.birthday,
        avatar=star.avatar,
        created_at=star.created_at,
        updated_at=star.updated_at,
        weibo_data=weibo,
        douyin_data=douyin,
        xiaohongshu_data=xiaohongshu,
        weibo_hot_search=[]
    )
    return result

@router.post("", response_model=StarResponse)
def create_star(star: StarCreate, db: Session = Depends(get_db)):
    db_star = Star(**star.model_dump())
    db.add(db_star)
    db.commit()
    db.refresh(db_star)
    return db_star

@router.put("/{star_id}", response_model=StarResponse)
def update_star(star_id: int, star: StarUpdate, db: Session = Depends(get_db)):
    db_star = db.query(Star).filter(Star.id == star_id).first()
    if not db_star:
        raise HTTPException(status_code=404, detail="明星不存在")
    
    for key, value in star.model_dump(exclude_unset=True).items():
        setattr(db_star, key, value)
    
    db_star.updated_at = datetime.now()
    db.commit()
    db.refresh(db_star)
    return db_star

@router.delete("/{star_id}")
def delete_star(star_id: int, db: Session = Depends(get_db)):
    db_star = db.query(Star).filter(Star.id == star_id).first()
    if not db_star:
        raise HTTPException(status_code=404, detail="明星不存在")
    
    db.delete(db_star)
    db.commit()
    return {"message": "删除成功"}

@router.put("/{star_id}/fans", response_model=StarResponse)
def update_fans_data(star_id: int, data: FanDataUpdate, db: Session = Depends(get_db)):
    star = db.query(Star).filter(Star.id == star_id).first()
    if not star:
        raise HTTPException(status_code=404, detail="明星不存在")
    
    if data.weibo_fans:
        weibo = db.query(WeiboData).filter(WeiboData.star_id == star_id).first()
        if not weibo:
            weibo = WeiboData(
                star_id=star_id,
                weibo_name=star.name,
                fans_count=data.weibo_fans,
                verified=data.weibo_verified or False,
                collect_date=datetime.now().date()
            )
            db.add(weibo)
        else:
            weibo.fans_count = data.weibo_fans
            weibo.verified = data.weibo_verified or False
            weibo.collect_date = datetime.now().date()
    
    if data.douyin_fans:
        douyin = db.query(DouyinData).filter(DouyinData.star_id == star_id).first()
        if not douyin:
            douyin = DouyinData(
                star_id=star_id,
                douyin_name=star.name,
                fans_count=data.douyin_fans,
                verified=data.douyin_verified or False,
                collect_date=datetime.now().date()
            )
            db.add(douyin)
        else:
            douyin.fans_count = data.douyin_fans
            douyin.verified = data.douyin_verified or False
            douyin.collect_date = datetime.now().date()
    
    if data.xiaohongshu_fans:
        xiaohongshu = db.query(XiaohongshuData).filter(XiaohongshuData.star_id == star_id).first()
        if not xiaohongshu:
            xiaohongshu = XiaohongshuData(
                star_id=star_id,
                xhs_name=star.name,
                fans_count=data.xiaohongshu_fans,
                verified=data.xiaohongshu_verified or False,
                has_official_account=data.xiaohongshu_verified or False,
                collect_date=datetime.now().date()
            )
            db.add(xiaohongshu)
        else:
            xiaohongshu.fans_count = data.xiaohongshu_fans
            xiaohongshu.verified = data.xiaohongshu_verified or False
            xiaohongshu.collect_date = datetime.now().date()
    
    if data.description:
        star.description = data.description
    
    
    db.commit()
    db.refresh(star)
    return star

@router.get("/export")
def export_stars(
    keyword: Optional[str] = None,
    level: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Star)
    
    if keyword:
        query = query.filter(Star.name.contains(keyword))
    if level:
        query = query.filter(Star.level == level)
    if category:
        query = query.filter(Star.category == category)
    
    stars = query.all()
    
    result = []
    for star in stars:
        weibo = db.query(WeiboData).filter(WeiboData.star_id == star.id).order_by(desc(WeiboData.collect_date)).first()
        douyin = db.query(DouyinData).filter(DouyinData.star_id == star.id).order_by(desc(DouyinData.collect_date)).first()
        xiaohongshu = db.query(XiaohongshuData).filter(XiaohongshuData.star_id == star.id).order_by(desc(Xiaohongshu.collect_date)).first()
        
        result.append({
            "name": star.name,
            "english_name": star.english_name,
            "gender": star.gender,
            "category": star.category,
            "level": star.level,
            "agency": star.agency,
            "description": star.description,
            "weibo_fans": weibo.fans_count if weibo else None,
            "douyin_fans": douyin.fans_count if douyin else None,
            "xiaohongshu_fans": xiaohongshu.fans_count if xiaohongshu else None,
        })
    
    return result
