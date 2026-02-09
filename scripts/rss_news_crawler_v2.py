#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RSS 新闻聚合器 V2 - 从 RSS 源获取新闻（改进版：添加时间过滤）
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime, timedelta
from dateutil import parser as date_parser
import os

class RSSNewsCrawler:
    """RSS 新闻聚合器"""
    
    def __init__(self, sector, hours=24):
        self.sector = sector
        self.hours = hours  # 时间范围（小时）
        self.results = []
        self.session = requests.Session()
        
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        })
        
        # RSS 新闻源列表（扩充版）
        self.rss_sources = {
            'healthcare': [
                {
                    'name': '人民网健康',
                    'url': 'http://health.people.com.cn/rss/health.xml'
                },
                {
                    'name': '新华网健康',
                    'url': 'http://www.xinhuanet.com/health/news_health.xml'
                },
                {
                    'name': '央视网健康',
                    'url': 'http://health.cctv.com/rss/health.xml'
                },
                {
                    'name': '健康报',
                    'url': 'http://www.jkb.com.cn/rss.xml'
                },
                {
                    'name': '丁香园',
                    'url': 'https://www.dxy.cn/feed'
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
                },
                {
                    'name': '中国教育新闻网',
                    'url': 'http://www.jyb.cn/rss/jyb.xml'
                },
                {
                    'name': '央视网教育',
                    'url': 'http://edu.cctv.com/rss/edu.xml'
                }
            ]
        }
    
    def parse_pubdate(self, pubdate_str):
        """
        解析发布时间
        
        参数:
            pubdate_str: 时间字符串
        
        返回:
            datetime 对象，解析失败返回 None
        """
        if not pubdate_str:
            return None
        
        try:
            # 使用 dateutil.parser 自动解析多种时间格式
            return date_parser.parse(pubdate_str)
        except:
            return None
    
    def is_recent_news(self, pubdate_str):
        """
        判断新闻是否在指定时间范围内
        
        参数:
            pubdate_str: 时间字符串
        
        返回:
            True 表示在时间范围内，False 表示不在
        """
        pub_datetime = self.parse_pubdate(pubdate_str)
        
        if not pub_datetime:
            # 如果无法解析时间，保守起见返回 False
            return False
        
        # 计算时间差
        now = datetime.now(pub_datetime.tzinfo) if pub_datetime.tzinfo else datetime.now()
        time_diff = now - pub_datetime
        
        # 判断是否在指定时间范围内
        return time_diff <= timedelta(hours=self.hours)
    
    def fetch_rss(self, rss_url, source_name):
        """
        获取 RSS 源（带时间过滤）
        
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
            filtered_count = 0
            
            for item in items:
                title_tag = item.find('title')
                link_tag = item.find('link')
                pubdate_tag = item.find('pubDate')
                
                if title_tag and link_tag:
                    title = title_tag.get_text().strip()
                    url = link_tag.get_text().strip()
                    pubdate = pubdate_tag.get_text().strip() if pubdate_tag else ''
                    
                    # 时间过滤：只保留最近的新闻
                    if pubdate and self.is_recent_news(pubdate):
                        news_items.append({
                            'title': title,
                            'url': url,
                            'source': source_name,
                            'pubdate': pubdate,
                            'date': datetime.now().strftime('%Y-%m-%d')
                        })
                    else:
                        filtered_count += 1
            
            print(f"  ✓ 找到 {len(news_items)} 条最近新闻（过滤掉 {filtered_count} 条旧新闻）")
            return news_items
            
        except Exception as e:
            print(f"  ✗ 获取失败: {e}")
            return []
    
    def crawl_all_sources(self):
        """爬取所有 RSS 源"""
        print(f"\n{'='*60}")
        print(f"开始爬取 RSS 新闻源（最近 {self.hours} 小时）")
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
            print(f"   发布时间: {news['pubdate']}")

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='RSS 新闻聚合器 V2（带时间过滤）')
    parser.add_argument('--sector', required=True, choices=['healthcare', 'education'], 
                        help='板块: healthcare 或 education')
    parser.add_argument('--hours', type=int, default=24,
                        help='时间范围（小时），默认24小时')
    
    args = parser.parse_args()
    
    crawler = RSSNewsCrawler(args.sector, args.hours)
    crawler.crawl_all_sources()
    crawler.save_results()

