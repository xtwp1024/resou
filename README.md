# 明星社交媒体数据采集系统

一个完整的明星社交媒体数据采集系统，支持微博、抖音、小红书三大平台的数据采集和管理。

## 功能特性

- **明星管理**：分层级管理明星信息（顶流/一线/二线/三线）
- **多平台采集**：支持微博、抖音、小红书三大平台
- **定时任务**：每日自动更新数据
- **数据可视化**：图表展示统计数据
- **API接口**：完整的RESTful API

## 技术栈

### 后端
- Python 3.10+
- FastAPI
- SQLAlchemy
- Playwright
- APScheduler

### 前端
- Vue 3
- Element Plus
- ECharts
- Pinia

## 项目结构

```
resou/
├── backend/                 # 后端代码
│   ├── app/
│   │   ├── api/            # API路由
│   │   ├── crawlers/       # 采集模块
│   │   ├── models/         # 数据模型
│   │   ├── schemas/        # Pydantic模型
│   │   ├── tasks/          # 定时任务
│   │   ├── config.py       # 配置
│   │   ├── database.py     # 数据库
│   │   └── main.py         # 入口
│   ├── requirements.txt
│   └── run.py
├── frontend/               # 前端代码
│   ├── src/
│   │   ├── api/           # API调用
│   │   ├── router/        # 路由
│   │   ├── views/         # 页面
│   │   ├── App.vue
│   │   └── main.js
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── data/                   # 数据文件
│   └── stars.json         # 初始明星名单
├── SPEC.md                # 项目规范
├── TASKS.md               # 任务清单
└── README.md
```

## 快速开始

### 1. 后端安装

```bash
cd backend

# 创建虚拟环境
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 安装依赖
pip install -r requirements.txt

# 安装 Playwright 浏览器
playwright install chromium

# 启动服务
python run.py
```

后端服务将在 http://localhost:8000 启动，API文档地址：http://localhost:8000/docs

### 2. 前端安装

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端服务将在 http://localhost:3000 启动

## API 接口

### 明星管理
- `GET /api/stars` - 获取明星列表
- `GET /api/stars/{id}` - 获取明星详情
- `POST /api/stars` - 添加明星
- `PUT /api/stars/{id}` - 更新明星
- `DELETE /api/stars/{id}` - 删除明星
- `GET /api/stars/stats` - 获取统计数据

### 数据采集
- `POST /api/crawl/weibo/{star_id}` - 采集微博数据
- `POST /api/crawl/douyin/{star_id}` - 采集抖音数据
- `POST /api/crawl/xiaohongshu/{star_id}` - 采集小红书数据
- `POST /api/crawl/all` - 采集全部明星数据
- `GET /api/crawl/status` - 获取采集状态

## 配置说明

### 后端配置 (backend/app/config.py)

```python
# 定时任务配置 - 每日凌晨2点执行
SCHEDULER_CONFIG = {
    "hour": 2,
    "minute": 0,
}

# 明星等级划分标准
STAR_LEVELS = {
    "dingliu": {"name": "顶流", "weibo_fans_min": 50000000},
    "yixian": {"name": "一线", "weibo_fans_min": 20000000},
    "erxian": {"name": "二线", "weibo_fans_min": 5000000},
    "sanxian": {"name": "三线", "weibo_fans_min": 1000000},
}
```

## 数据采集说明

由于各平台反爬机制，采集模块采用以下策略：

1. **微博**：通过微博搜索页面获取公开数据
2. **抖音**：通过抖音搜索页面获取公开数据
3. **小红书**：通过小红书搜索页面获取公开数据

**注意事项**：
- 首次运行需要安装 Playwright 浏览器
- 采集频率建议控制在合理范围
- 部分明星可能没有开通某些平台账号

## 使用流程

1. **添加明星**：在前端界面或通过API添加明星信息
2. **采集数据**：手动触发或等待定时任务自动采集
3. **查看数据**：在明星详情页查看各平台数据
4. **数据分析**：通过仪表盘查看统计数据和趋势

## 开发计划

- [ ] 添加更多平台支持（B站、快手等）
- [ ] 数据导出功能（Excel/CSV）
- [ ] 粉丝趋势图表
- [ ] 热搜记录采集
- [ ] 数据对比功能
- [ ] 移动端适配

## License

MIT
