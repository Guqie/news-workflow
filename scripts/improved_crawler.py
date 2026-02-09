#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
改进版滚动新闻爬虫 - 两级关键词匹配策略
"""

import json
import os
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import time

class ImprovedRollingNewsCrawler:
    """改进版滚动新闻爬虫 - 提高匹配率"""
    
    def __init__(self, sector):
        self.sector = sector
        self.config = self.load_config()
        self.results = []
        self.session = requests.Session()
        
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        })
        
        # 核心关键词（专业词汇）
        self.core_keywords = self.config['sectors'][sector]['keywords']
        
        # 辅助关键词（提高召回率）
        self.auxiliary_keywords = ['产业', '发展', '创新', '服务', '保障', '改革', '建设']
    
    def load_config(self):
        """加载配置文件"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(script_dir, '../references/config.json')
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def match_keywords(self, title):
        """
        两级关键词匹配策略
        
        规则：
        1. 必须包含至少1个核心关键词
        2. 或者包含2个以上辅助关键词
        """
        # 检查核心关键词
        core_match_count = 0
        for keyword in self.core_keywords:
            if keyword in title:
                core_match_count += 1
        
        if core_match_count >= 1:
            return True
        
        # 检查辅助关键词
        aux_match_count = 0
        for keyword in self.auxiliary_keywords:
            if keyword in title:
                aux_match_count += 1
        
        if aux_match_count >= 2:
            return True
        
        return False
    
    def crawl_rolling_news(self, url, max_pages=3):
        """爬取滚动新闻"""
        print(f"\n🔍 爬取滚动新闻: {url}")
        print(f"📋 匹配策略: 核心词({len(self.core_keywords)}个) + 辅助词({len(self.auxiliary_keywords)}个)")
        
        for page in range(1, max_pages + 1):
            print(f"\n  📄 第 {page} 页...")
            
            page_url = self.build_page_url(url, page)
            
            try:
                response = self.session.get(page_url, timeout=10)
                
                if 'people.com.cn' in page_url:
                    response.encoding = 'gb2312'
                else:
                    response.encoding = 'utf-8'
                
                soup = BeautifulSoup(response.text, 'html.parser')
                news_items = self.extract_news_list(soup, url)
                
                matched_count = 0
                for item in news_items:
                    if self.match_keywords(item['title']):
                        self.results.append(item)
                        matched_count += 1
                
                print(f"     ✓ 找到 {len(news_items)} 条新闻，匹配 {matched_count} 条")
                
                time.sleep(1)
                
            except Exception as e:
                print(f"     ✗ 爬取失败: {e}")
                break
        
        self.deduplicate()
    
    def build_page_url(self, base_url, page):
        """构造翻页URL"""
        if 'people.com.cn' in base_url:
            if page == 1:
                return base_url
            else:
                return base_url.replace('index.html', f'index{page}.html')
        elif 'sina.com.cn' in base_url:
            return base_url.replace('page=1', f'page={page}')
        else:
            separator = '&' if '?' in base_url else '?'
            return f"{base_url}{separator}page={page}"
