"""
Pydantic模型定义（用于API请求/响应）
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class NewsItemBase(BaseModel):
    """新闻基础模型"""
    title: str
    content: Optional[str] = None
    source: Optional[str] = None
    source_url: Optional[str] = None
    column_name: str


class NewsItemCreate(NewsItemBase):
    """创建新闻的请求模型"""
    publish_date: Optional[datetime] = None


class NewsItemUpdate(BaseModel):
    """更新新闻的请求模型"""
    edited_title: Optional[str] = None
    status: Optional[str] = None
    score: Optional[float] = None


class NewsItemResponse(NewsItemBase):
    """新闻响应模型"""
    id: str
    edited_title: Optional[str] = None
    score: float
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class NewsListResponse(BaseModel):
    """新闻列表响应"""
    total: int
    items: List[NewsItemResponse]
