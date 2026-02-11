#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google 新闻搜索爬虫 - 获取24小时内的最新新闻
"""

from gnews import GNews
import json
import os
from datetime import datetime, timedelta

class GoogleNewsCrawler:
    """Google 新闻搜索爬虫"""
    
    def __init__(self, sector, hours=24):
        self.sector = sector
        self.hours = hours
        self.results = []
        
        # 初始化 GNews
        self.google_news = GNews(
            language='zh',  # 中文
            country='CN',   # 中国
            period=f'{hours}h',  # 时间范围
            max_results=100  # 每个关键词最多100条
        )
        
        self.config = self.load_config()
    
    def load_config(self):
        """加载配置文件"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(script_dir, '../references/config.json')
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def search_news(self, keyword):
        """
        搜索新闻
        
        参数:
            keyword: 搜索关键词
        """
        print(f"\n🔍 搜索 Google 新闻: {keyword}")
        
        try:
            # 搜索新闻
            news_list = self.google_news.get_news(keyword)
            
            news_items = []
            for news in news_list:
                news_items.append({
                    'title': news.get('title', ''),
                    'url': news.get('url', ''),
                    'source': news.get('publisher', {}).get('title', '未知来源'),
                    'published_date': news.get('published date', ''),
                    'keyword': keyword,
                    'date': datetime.now().strftime('%Y-%m-%d')
                })
            
            print(f"  ✓ 找到 {len(news_items)} 条新闻")
            return news_items
            
        except Exception as e:
            print(f"  ✗ 搜索失败: {e}")
            return []
    
    def search_with_keywords(self, keywords):
        """使用多个关键词搜索"""
        print(f"\n{'='*60}")
        print(f"开始搜索 Google 新闻 - {self.config['sectors'][self.sector]['name']}")
        print(f"时间范围: 最近 {self.hours} 小时")
        print(f"{'='*60}")
        
        for keyword in keywords:
            news_items = self.search_news(keyword)
            self.results.extend(news_items)
        
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
        output_file = os.path.join(output_dir, f'{self.sector}_google_{date_str}.json')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 已保存到: {output_file}")
        print(f"📊 共保存: {len(self.results)} 条新闻")
        
        # 打印前5条标题
        print(f"\n📰 前5条新闻标题：")
        for i, news in enumerate(self.results[:5], 1):
            print(f"{i}. {news['title']}")
            print(f"   来源: {news['source']} | 发布: {news['published_date']}")

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Google 新闻搜索爬虫')
    parser.add_argument('--sector', required=True, 
                        choices=['healthcare', 'education', 'strategic_emerging', 'hightech'], 
                        help='板块: healthcare, education, strategic_emerging, hightech')
    parser.add_argument('--hours', type=int, default=24, help='时间范围（小时）')
    parser.add_argument('--keywords', nargs='+', help='搜索关键词列表')
    
    args = parser.parse_args()
    
    crawler = GoogleNewsCrawler(args.sector, args.hours)
    
    # 如果没有指定关键词，使用默认的第一优先级关键词
    if not args.keywords:
        if args.sector == 'healthcare':
            keywords = ["医药产业", "生物医药", "医疗健康", "医保改革"]
        elif args.sector == 'education':
            keywords = ["人才政策", "教育改革", "人才培养", "职业教育"]
        elif args.sector == 'strategic_emerging':
            keywords = ["战略新兴产业", "新能源", "新材料", "数字经济"]
        elif args.sector == 'hightech':
            keywords = ["高科技产业", "人工智能", "芯片", "半导体"]
    else:
        keywords = args.keywords
    
    crawler.search_with_keywords(keywords)
    crawler.save_results()

