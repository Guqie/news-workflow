#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新闻去重模块 - 基于标题相似度的智能去重
"""

from difflib import SequenceMatcher
import re

class NewsDeduplicator:
    """新闻去重器"""
    
    def __init__(self, similarity_threshold=0.8):
        """
        初始化去重器
        
        Args:
            similarity_threshold: 相似度阈值，默认0.8（80%）
        """
        self.similarity_threshold = similarity_threshold
    
    def normalize_title(self, title):
        """标准化标题"""
        if not title:
            return ""
        
        # 转小写
        title = title.lower()
        
        # 去除多余空格
        title = re.sub(r'\s+', ' ', title).strip()
        
        # 去除常见的标点符号
        title = re.sub(r'[，。！？、；：""''（）《》【】\[\]().,!?;:\'"<>{}]', '', title)
        
        return title
    
    def calculate_similarity(self, title1, title2):
        """计算两个标题的相似度"""
        norm_title1 = self.normalize_title(title1)
        norm_title2 = self.normalize_title(title2)
        
        if not norm_title1 or not norm_title2:
            return 0.0
        
        # 使用SequenceMatcher计算相似度
        similarity = SequenceMatcher(None, norm_title1, norm_title2).ratio()
        return similarity
    
    def is_duplicate(self, title1, title2):
        """判断两个标题是否重复"""
        similarity = self.calculate_similarity(title1, title2)
        return similarity >= self.similarity_threshold
    
    def deduplicate(self, news_list):
        """
        对新闻列表进行去重
        
        Args:
            news_list: 新闻列表，每条新闻需要有'title'字段
            
        Returns:
            去重后的新闻列表
        """
        if not news_list:
            return []
        
        unique_news = []
        removed_count = 0
        
        for news in news_list:
            title = news.get('title', '')
            if not title:
                continue
            
            # 检查是否与已有新闻重复
            is_dup = False
            for existing_news in unique_news:
                existing_title = existing_news.get('title', '')
                if self.is_duplicate(title, existing_title):
                    is_dup = True
                    removed_count += 1
                    break
            
            if not is_dup:
                unique_news.append(news)
        
        print(f"  🔄 去重: 移除 {removed_count} 条相似新闻")
        print(f"  📊 去重后: {len(unique_news)} 条新闻")
        
        return unique_news
