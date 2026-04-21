from datetime import datetime, date
from sqlalchemy import Column, Integer, String, BigInteger, Boolean, DateTime, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Star(Base):
    __tablename__ = "stars"

    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    english_name = Column(String(100), nullable=True)
    gender = Column(String(10), nullable=True)
    category = Column(String(50), nullable=True)
    level = Column(String(20), nullable=True, index=True)
    agency = Column(String(200), nullable=True)
    birthday = Column(Date, nullable=True)
    avatar = Column(String(500), nullable=True)
    description = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    weibo_data = relationship("WeiboData", back_populates="star", cascade="all, delete-orphan")
    douyin_data = relationship("DouyinData", back_populates="star", cascade="all, delete-orphan")
    xiaohongshu_data = relationship("XiaohongshuData", back_populates="star", cascade="all, delete-orphan")
    weibo_hot_search = relationship("WeiboHotSearch", back_populates="star", cascade="all, delete-orphan")

class WeiboData(Base):
    __tablename__ = "weibo_data"

    id = Column(Integer, primary_key=True, index=True)
    star_id = Column(Integer, ForeignKey("stars.id"), nullable=False, index=True)
    weibo_id = Column(String(50), nullable=True)
    weibo_name = Column(String(100), nullable=True)
    fans_count = Column(BigInteger, default=0)
    following_count = Column(Integer, default=0)
    posts_count = Column(Integer, default=0)
    verified = Column(Boolean, default=False)
    verified_type = Column(Integer, default=0)
    verified_reason = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)
    avatar = Column(String(500), nullable=True)
    collect_date = Column(Date, default=date.today, index=True)
    created_at = Column(DateTime, default=datetime.now)

    star = relationship("Star", back_populates="weibo_data")

class WeiboHotSearch(Base):
    __tablename__ = "weibo_hot_search"

    id = Column(Integer, primary_key=True, index=True)
    star_id = Column(Integer, ForeignKey("stars.id"), nullable=False, index=True)
    keyword = Column(String(200), nullable=False)
    rank = Column(Integer, nullable=True)
    hot_value = Column(BigInteger, default=0)
    on_list_time = Column(DateTime, nullable=True)
    off_list_time = Column(DateTime, nullable=True)
    duration_hours = Column(Integer, default=0)
    collect_date = Column(Date, default=date.today, index=True)
    created_at = Column(DateTime, default=datetime.now)

    star = relationship("Star", back_populates="weibo_hot_search")

class DouyinData(Base):
    __tablename__ = "douyin_data"

    id = Column(Integer, primary_key=True, index=True)
    star_id = Column(Integer, ForeignKey("stars.id"), nullable=False, index=True)
    douyin_id = Column(String(50), nullable=True)
    douyin_name = Column(String(100), nullable=True)
    unique_id = Column(String(100), nullable=True)
    fans_count = Column(BigInteger, default=0)
    following_count = Column(Integer, default=0)
    likes_count = Column(BigInteger, default=0)
    video_count = Column(Integer, default=0)
    verified = Column(Boolean, default=False)
    avatar = Column(String(500), nullable=True)
    signature = Column(Text, nullable=True)
    collect_date = Column(Date, default=date.today, index=True)
    created_at = Column(DateTime, default=datetime.now)

    star = relationship("Star", back_populates="douyin_data")

class XiaohongshuData(Base):
    __tablename__ = "xiaohongshu_data"

    id = Column(Integer, primary_key=True, index=True)
    star_id = Column(Integer, ForeignKey("stars.id"), nullable=False, index=True)
    xhs_id = Column(String(50), nullable=True)
    xhs_name = Column(String(100), nullable=True)
    fans_count = Column(BigInteger, default=0)
    following_count = Column(Integer, default=0)
    likes_collects_count = Column(BigInteger, default=0)
    notes_count = Column(Integer, default=0)
    verified = Column(Boolean, default=False)
    has_official_account = Column(Boolean, default=False)
    avatar = Column(String(500), nullable=True)
    signature = Column(Text, nullable=True)
    collect_date = Column(Date, default=date.today, index=True)
    created_at = Column(DateTime, default=datetime.now)

    star = relationship("Star", back_populates="xiaohongshu_data")
