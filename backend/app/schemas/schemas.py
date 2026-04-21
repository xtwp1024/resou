from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel

class StarBase(BaseModel):
    name: str
    english_name: Optional[str] = None
    gender: Optional[str] = None
    category: Optional[str] = None
    level: Optional[str] = None
    agency: Optional[str] = None
    birthday: Optional[date] = None
    avatar: Optional[str] = None

class StarCreate(StarBase):
    pass

class StarUpdate(StarBase):
    name: Optional[str] = None

class StarResponse(StarBase):
    id: int
    created_at: datetime
    updated_at: datetime
    weibo_fans: Optional[int] = None
    douyin_fans: Optional[int] = None
    xiaohongshu_fans: Optional[int] = None

    class Config:
        from_attributes = True

class StarListResponse(BaseModel):
    total: int
    items: List[StarResponse]

class WeiboDataBase(BaseModel):
    weibo_id: Optional[str] = None
    weibo_name: Optional[str] = None
    fans_count: int = 0
    following_count: int = 0
    posts_count: int = 0
    verified: bool = False
    verified_type: int = 0
    verified_reason: Optional[str] = None
    description: Optional[str] = None
    avatar: Optional[str] = None

class WeiboDataResponse(WeiboDataBase):
    id: int
    star_id: int
    collect_date: date
    created_at: datetime

    class Config:
        from_attributes = True

class WeiboHotSearchBase(BaseModel):
    keyword: str
    rank: Optional[int] = None
    hot_value: int = 0
    on_list_time: Optional[datetime] = None
    off_list_time: Optional[datetime] = None
    duration_hours: int = 0

class WeiboHotSearchResponse(WeiboHotSearchBase):
    id: int
    star_id: int
    collect_date: date
    created_at: datetime

    class Config:
        from_attributes = True

class DouyinDataBase(BaseModel):
    douyin_id: Optional[str] = None
    douyin_name: Optional[str] = None
    unique_id: Optional[str] = None
    fans_count: int = 0
    following_count: int = 0
    likes_count: int = 0
    video_count: int = 0
    verified: bool = False
    avatar: Optional[str] = None
    signature: Optional[str] = None

class DouyinDataResponse(DouyinDataBase):
    id: int
    star_id: int
    collect_date: date
    created_at: datetime

    class Config:
        from_attributes = True

class XiaohongshuDataBase(BaseModel):
    xhs_id: Optional[str] = None
    xhs_name: Optional[str] = None
    fans_count: int = 0
    following_count: int = 0
    likes_collects_count: int = 0
    notes_count: int = 0
    verified: bool = False
    has_official_account: bool = False
    avatar: Optional[str] = None
    signature: Optional[str] = None

class XiaohongshuDataResponse(XiaohongshuDataBase):
    id: int
    star_id: int
    collect_date: date
    created_at: datetime

    class Config:
        from_attributes = True

class StarDetailResponse(StarResponse):
    weibo_data: Optional[WeiboDataResponse] = None
    douyin_data: Optional[DouyinDataResponse] = None
    xiaohongshu_data: Optional[XiaohongshuDataResponse] = None
    weibo_hot_search: List[WeiboHotSearchResponse] = []

class CrawlResult(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None

class StatsResponse(BaseModel):
    total_stars: int
    by_level: dict
    by_category: dict
    last_crawl_time: Optional[datetime] = None
