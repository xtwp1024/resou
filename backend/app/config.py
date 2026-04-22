import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/data/resou.db")

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

CORS_CONFIG = {
    "allow_origins": os.getenv(
        "ALLOWED_ORIGINS", 
        "http://localhost:5173,http://127.0.0.1:5173"
    ).split(","),
    "allow_credentials": True,
    "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    "allow_headers": ["*"],
}

CRAWLER_CONFIG = {
    "weibo": {
        "base_url": "https://weibo.com",
        "search_url": "https://s.weibo.com/user",
        "timeout": 30,
    },
    "douyin": {
        "base_url": "https://www.douyin.com",
        "search_url": "https://www.douyin.com/search",
        "timeout": 30,
    },
    "xiaohongshu": {
        "base_url": "https://www.xiaohongshu.com",
        "search_url": "https://www.xiaohongshu.com/search_result",
        "timeout": 30,
    },
}

SCHEDULER_CONFIG = {
    "hour": 2,
    "minute": 0,
}

STAR_LEVELS = {
    "dingliu": {
        "name": "顶流",
        "weibo_fans_min": 50000000,
        "douyin_fans_min": 30000000,
    },
    "yixian": {
        "name": "一线",
        "weibo_fans_min": 20000000,
        "weibo_fans_max": 50000000,
        "douyin_fans_min": 10000000,
        "douyin_fans_max": 30000000,
    },
    "erxian": {
        "name": "二线",
        "weibo_fans_min": 5000000,
        "weibo_fans_max": 20000000,
        "douyin_fans_min": 3000000,
        "douyin_fans_max": 10000000,
    },
    "sanxian": {
        "name": "三线",
        "weibo_fans_min": 1000000,
        "weibo_fans_max": 5000000,
        "douyin_fans_min": 500000,
        "douyin_fans_max": 3000000,
    },
}

MINIMAX_CONFIG = {
    "api_key": os.getenv("MINIMAX_API_KEY", ""),
    "group_id": os.getenv("MINIMAX_GROUP_ID", ""),
    "base_url": "https://api.minimaxi.com/v1/chat/completions",
    "model": "MiniMax-M2.5",
}
