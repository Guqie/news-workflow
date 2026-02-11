"""
新闻相关API接口
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models import NewsItem
from ..schemas import NewsItemCreate, NewsItemUpdate, NewsItemResponse, NewsListResponse

router = APIRouter()


@router.get("/", response_model=NewsListResponse)
async def get_news_list(
    column: Optional[str] = None,
    status: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """获取新闻列表"""
    query = db.query(NewsItem)
    
    if column:
        query = query.filter(NewsItem.column_name == column)
    if status:
        query = query.filter(NewsItem.status == status)
    
    total = query.count()
    items = query.order_by(NewsItem.created_at.desc()).offset(skip).limit(limit).all()
    
    return NewsListResponse(total=total, items=items)


@router.get("/{news_id}", response_model=NewsItemResponse)
async def get_news_detail(news_id: str, db: Session = Depends(get_db)):
    """获取新闻详情"""
    news = db.query(NewsItem).filter(NewsItem.id == news_id).first()
    if not news:
        raise HTTPException(status_code=404, detail="新闻不存在")
    return news
