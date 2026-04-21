from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db
from app.api import stars, crawl, ai
from app.tasks import start_scheduler

app = FastAPI(
    title="明星数据采集系统",
    description="采集微博、抖音、小红书明星数据",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stars.router)
app.include_router(crawl.router)
app.include_router(ai.router)

@app.on_event("startup")
async def startup_event():
    init_db()
    start_scheduler()

@app.on_event("shutdown")
async def shutdown_event():
    from app.tasks import stop_scheduler
    stop_scheduler()

@app.get("/")
def root():
    return {"message": "明星数据采集系统 API", "docs": "/docs"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
