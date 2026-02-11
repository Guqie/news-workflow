"""
任务相关API接口
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter()


@router.post("/crawl")
async def trigger_crawl_task(
    column: str,
    db: Session = Depends(get_db)
):
    """触发采集任务"""
    # TODO: 实现采集任务逻辑
    return {
        "status": "success",
        "message": f"采集任务已触发: {column}",
        "task_id": "temp_task_id"
    }


@router.get("/status/{task_id}")
async def get_task_status(task_id: str):
    """查询任务状态"""
    # TODO: 实现任务状态查询
    return {
        "task_id": task_id,
        "status": "running",
        "progress": 50
    }
