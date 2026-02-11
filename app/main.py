"""
FastAPI主应用入口
"""
from fastapi import FastAPI
from .database import init_db
from .api import news, tasks

# 创建FastAPI应用
app = FastAPI(
    title="智库新闻自动化系统",
    description="新闻采集、处理、管理API",
    version="1.0.0"
)

# 启动时初始化数据库
@app.on_event("startup")
async def startup_event():
    init_db()
    print("✅ 数据库初始化完成")

# 注册路由
app.include_router(news.router, prefix="/api/news", tags=["新闻"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["任务"])

# 根路径
@app.get("/")
async def root():
    return {
        "message": "智库新闻自动化系统API",
        "version": "1.0.0",
        "docs": "/docs"
    }
