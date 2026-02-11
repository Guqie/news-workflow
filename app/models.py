"""
数据库模型定义
"""
from sqlalchemy import Column, String, Integer, Float, DateTime, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import uuid

Base = declarative_base()


class NewsItem(Base):
    """新闻条目模型"""
    __tablename__ = "news_items"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(500), nullable=False)
    edited_title = Column(String(500))
    content = Column(Text)
    source = Column(String(200))
    source_url = Column(Text)
    publish_date = Column(DateTime)
    column_name = Column(String(100))
    score = Column(Float, default=0)
    status = Column(String(50), default='pending')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class Keyword(Base):
    """关键词模型"""
    __tablename__ = "keywords"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    news_id = Column(String, nullable=False)
    keyword = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
