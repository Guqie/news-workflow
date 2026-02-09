#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RSS 新闻聚合器 - 从 RSS 源获取新闻
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
import os

class RSSNewsCrawler:
    """RSS 新闻聚合器"""
    
    def __init__(self, sector):
        self.sector = sector
        self.results = []
        self.session = requests.Session()
        
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        })
        
        # RSS 新闻源列表
        self.rss_sources = {
            'healthcare': [
                {
                    'name': '人民网健康',
                    'url': 'http://health.people.com.cn/rss/health.xml'
                },
                {
                    'name': '新华网健康',
                    'url': 'http://www.xinhuanet.com/health/news_health.xml'
                }
            ],
            'education': [
                {
                    'name': '人民网教育',
                    'url': 'http://edu.people.com.cn/rss/edu.xml'
                },
                {
                    'name': '新华网教育',
                    'url': 'http://www.xinhuanet.com/edu/news_edu.xml'
                }
            ]
        }
    
    def fetch_rss(self, rss_url, source_name):
        """
        获取 RSS 源
        
        参数:
            rss_url: RSS 源 URL
            source_name: 来源名称
        """
        print(f"\n🔍 获取 RSS: {source_name}")
        
        try:
            response = self.session.get(rss_url, timeout=10)
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.text, 'xml')
            items = soup.find_all('item')
            
            news_items = []
            for item in items:
                title_tag = item.find('title')
                link_tag = item.find('link')
                pubdate_tag = item.find('pubDate')
                
                if title_tag and link_tag:
                    title = title_tag.get_text().strip()
                    url = link_tag.get_text().strip()
                    pubdate = pubdate_tag.get_text().strip() if pubdate_tag else ''
                    
                    news_items.append({
                        'title': title,
                        'url': url,
                        'source': source_name,
                        'pubdate': pubdate,
                        'date': datetime.now().strftime('%Y-%m-%d')
                    })
            
            print(f"  ✓ 找到 {len(news_items)} 条新闻")
            return news_items
            
        except Exception as e:
            print(f"  ✗ 获取失败: {e}")
            return []
    
    def crawl_all_sources(self):
        """爬取所有 RSS 源"""
        print(f"\n{'='*60}")
        print(f"开始爬取 RSS 新闻源")
        print(f"{'='*60}")
        
        sources = self.rss_sources.get(self.sector, [])
        
        for source in sources:
            news_items = self.fetch_rss(source['url'], source['name'])
            self.results.extend(news_items)
            time.sleep(1)
        
        # 去重
        self.deduplicate()
    
    def deduplicate(self):
        """去重"""
        seen_titles = set()
        unique_results = []
        
        for news in self.results:
            title = news['title']
            if title not in seen_titles:
                seen_titles.add(title)
                unique_results.append(news)
        
        removed = len(self.results) - len(unique_results)
        if removed > 0:
            print(f"\n🔄 去重: 移除 {removed} 条重复新闻")
        
        self.results = unique_results
    
    def save_results(self):
        """保存结果"""
        if not self.results:
            print("\n⚠️  没有找到任何新闻")
            return
        
        # 创建输出目录
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(script_dir, '../data/raw')
        os.makedirs(output_dir, exist_ok=True)
        
        # 保存为 JSON
        date_str = datetime.now().strftime('%Y%m%d')
        output_file = os.path.join(output_dir, f'{self.sector}_rss_{date_str}.json')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 已保存到: {output_file}")
        print(f"📊 共保存: {len(self.results)} 条新闻")
        
        # 打印前5条标题
        print(f"\n📰 前5条新闻标题：")
        for i, news in enumerate(self.results[:5], 1):
            print(f"{i}. {news['title']}")

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='RSS 新闻聚合器')
    parser.add_argument('--sector', required=True, choices=['healthcare', 'education'], 
                        help='板块: healthcare 或 education')
    
    args = parser.parse_args()
    
    crawler = RSSNewsCrawler(args.sector)
    crawler.crawl_all_sources()
    crawler.save_results()
