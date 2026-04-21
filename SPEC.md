# 明星数据采集系统 - 项目规范

## 1. 项目概述

### 1.1 项目目标
构建一个完整的明星社交媒体数据采集系统，支持：
- 全国明星数据的分层级管理（顶流、一线、二线、三线）
- 三大平台数据采集：微博、抖音、小红书
- 每日自动更新数据
- 快速查询和调取功能

### 1.2 核心功能
1. **明星管理**：添加、编辑、删除明星信息，支持分层级分类
2. **数据采集**：自动采集微博、抖音、小红书的粉丝数据
3. **数据存储**：历史数据记录，支持趋势分析
4. **数据展示**：Web界面展示，支持搜索、筛选、排序
5. **定时任务**：每日自动更新数据

---

## 2. 数据字段规范

### 2.1 明星基础信息
| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | integer | 主键ID |
| name | string | 明星姓名 |
| english_name | string | 英文名（可选） |
| gender | string | 性别（男/女） |
| category | string | 类型（演员/歌手/主持人/偶像等） |
| level | string | 等级（顶流/一线/二线/三线） |
| agency | string | 经纪公司 |
| birthday | date | 出生日期 |
| avatar | string | 头像URL |
| created_at | datetime | 创建时间 |
| updated_at | datetime | 更新时间 |

### 2.2 微博数据
| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | integer | 主键ID |
| star_id | integer | 关联明星ID |
| weibo_id | string | 微博用户ID |
| weibo_name | string | 微博昵称 |
| fans_count | bigint | 粉丝数 |
| following_count | integer | 关注数 |
| posts_count | integer | 微博数 |
| verified | boolean | 是否认证 |
| verified_type | integer | 认证类型 |
| verified_reason | string | 认证信息 |
| description | string | 简介 |
| avatar | string | 头像URL |
| collect_date | date | 采集日期 |
| created_at | datetime | 创建时间 |

### 2.3 微博热搜记录
| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | integer | 主键ID |
| star_id | integer | 关联明星ID |
| keyword | string | 热搜关键词 |
| rank | integer | 最高排名 |
| hot_value | bigint | 热度值 |
| on_list_time | datetime | 上榜时间 |
| off_list_time | datetime | 下榜时间 |
| duration_hours | float | 在榜时长（小时） |
| collect_date | date | 采集日期 |
| created_at | datetime | 创建时间 |

### 2.4 抖音数据
| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | integer | 主键ID |
| star_id | integer | 关联明星ID |
| douyin_id | string | 抖音用户ID |
| douyin_name | string | 抖音昵称 |
| unique_id | string | 抖音号 |
| fans_count | bigint | 粉丝数 |
| following_count | integer | 关注数 |
| likes_count | bigint | 获赞数 |
| video_count | integer | 视频数 |
| verified | boolean | 是否认证 |
| avatar | string | 头像URL |
| signature | string | 签名 |
| collect_date | date | 采集日期 |
| created_at | datetime | 创建时间 |

### 2.5 小红书数据
| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | integer | 主键ID |
| star_id | integer | 关联明星ID |
| xhs_id | string | 小红书用户ID |
| xhs_name | string | 小红书昵称 |
| fans_count | bigint | 粉丝数 |
| following_count | integer | 关注数 |
| likes_collects_count | bigint | 获赞与收藏数 |
| notes_count | integer | 笔记数 |
| verified | boolean | 是否认证 |
| avatar | string | 头像URL |
| signature | string | 签名 |
| has_official_account | boolean | 是否有官方账号 |
| collect_date | date | 采集日期 |
| created_at | datetime | 创建时间 |

---

## 3. 明星等级划分标准

### 3.1 顶流明星
- 微博粉丝 > 5000万
- 或抖音粉丝 > 3000万
- 或近期有3个以上热搜

### 3.2 一线明星
- 微博粉丝 2000万-5000万
- 或抖音粉丝 1000万-3000万

### 3.3 二线明星
- 微博粉丝 500万-2000万
- 或抖音粉丝 300万-1000万

### 3.4 三线明星
- 微博粉丝 100万-500万
- 或抖音粉丝 50万-300万

---

## 4. 技术架构

### 4.1 技术栈选型
```
后端：Python + FastAPI
数据库：SQLite（开发）/ PostgreSQL（生产）
数据采集：Playwright + BeautifulSoup
定时任务：APScheduler
前端：Vue 3 + Element Plus
API文档：Swagger（FastAPI内置）
```

### 4.2 项目结构
```
resou/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI入口
│   │   ├── config.py            # 配置文件
│   │   ├── database.py          # 数据库连接
│   │   ├── models/              # 数据模型
│   │   │   ├── __init__.py
│   │   │   ├── star.py
│   │   │   ├── weibo.py
│   │   │   ├── douyin.py
│   │   │   └── xiaohongshu.py
│   │   ├── schemas/             # Pydantic模型
│   │   │   ├── __init__.py
│   │   │   ├── star.py
│   │   │   ├── weibo.py
│   │   │   ├── douyin.py
│   │   │   └── xiaohongshu.py
│   │   ├── api/                 # API路由
│   │   │   ├── __init__.py
│   │   │   ├── stars.py
│   │   │   ├── weibo.py
│   │   │   ├── douyin.py
│   │   │   ├── xiaohongshu.py
│   │   │   └── tasks.py
│   │   ├── services/            # 业务逻辑
│   │   │   ├── __init__.py
│   │   │   ├── star_service.py
│   │   │   └── data_service.py
│   │   ├── crawlers/            # 采集模块
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── weibo_crawler.py
│   │   │   ├── douyin_crawler.py
│   │   │   └── xiaohongshu_crawler.py
│   │   └── tasks/               # 定时任务
│   │       ├── __init__.py
│   │       └── scheduler.py
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── src/
│   │   ├── views/
│   │   ├── components/
│   │   ├── api/
│   │   ├── stores/
│   │   └── App.vue
│   ├── package.json
│   └── vite.config.js
├── data/
│   └── stars.json               # 初始明星名单
├── docs/
│   └── API.md
├── SPEC.md
├── TASKS.md
└── README.md
```

---

## 5. API接口设计

### 5.1 明星管理
- `GET /api/stars` - 获取明星列表（支持分页、筛选、排序）
- `GET /api/stars/{id}` - 获取明星详情
- `POST /api/stars` - 添加明星
- `PUT /api/stars/{id}` - 更新明星信息
- `DELETE /api/stars/{id}` - 删除明星
- `GET /api/stars/stats` - 获取统计数据

### 5.2 数据采集
- `POST /api/crawl/weibo/{star_id}` - 采集单个明星微博数据
- `POST /api/crawl/douyin/{star_id}` - 采集单个明星抖音数据
- `POST /api/crawl/xiaohongshu/{star_id}` - 采集单个明星小红书数据
- `POST /api/crawl/all` - 采集所有明星数据
- `GET /api/crawl/status` - 获取采集任务状态

### 5.3 数据查询
- `GET /api/weibo/{star_id}` - 获取微博数据历史
- `GET /api/douyin/{star_id}` - 获取抖音数据历史
- `GET /api/xiaohongshu/{star_id}` - 获取小红书数据历史
- `GET /api/trends/{star_id}` - 获取粉丝趋势数据

---

## 6. 数据采集策略

### 6.1 采集频率
- 每日凌晨2:00自动采集所有明星数据
- 支持手动触发采集
- 支持单独采集某个明星

### 6.2 采集方式
由于各平台反爬机制，采用以下策略：
1. **微博**：通过搜索获取公开数据
2. **抖音**：通过搜索获取公开数据
3. **小红书**：通过搜索获取公开数据

### 6.3 数据验证
- 验证账号是否为官方认证账号
- 记录采集时间戳
- 异常数据标记和人工审核

---

## 7. 前端界面设计

### 7.1 主要页面
1. **仪表盘**：数据概览、统计图表
2. **明星列表**：支持搜索、筛选、排序
3. **明星详情**：展示单个明星的完整数据
4. **数据对比**：多个明星数据对比
5. **趋势分析**：粉丝增长趋势图表
6. **任务管理**：查看采集任务状态

### 7.2 功能特性
- 响应式设计
- 数据导出（Excel/CSV）
- 批量操作
- 数据可视化图表
