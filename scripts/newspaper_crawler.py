#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Newspaper4k 新闻提取器 - 从新闻网站提取文章
"""

from newspaper import Article, Source
import json
import os
from datetime import datetime, timedelta

class Newspaper4kCrawler:
    """Newspaper4k 新闻提取器"""
    
    def __init__(self, sector, hours=24):
        self.sector = sector
        self.hours = hours
        self.results = []
        
        # 新闻源列表
        self.news_sources = {
            'healthcare': [
                'https://www.jkb.com.cn',  # 健康报
                'https://news.pharmnet.com.cn',  # 医药网
            ],
            'education': [
                'http://edu.people.com.cn',  # 人民网教育
                'https://news.sciencenet.cn',  # 科学网
            ]
        }
    
    def crawl_source(self, source_url):
        """爬取新闻源"""
        print(f"\n🔍 爬取新闻源: {source_url}")
        
        try:
            # 构建新闻源
            source = Source(source_url, language='zh')
            source.build()
            
            news_items = []
            cutoff_time = datetime.now() - timedelta(hours=self.hours)
            
            # 遍历文章
            for article in source.articles[:50]:  # 限制50篇
                try:
                    article.download()
                    article.parse()
                    
                    # 检查发布时间
                    if article.publish_date:
                        if article.publish_date.replace(tzinfo=None) < cutoff_time:
                            continue
                    
                    news_items.append({
                        'title': article.title,
                        'url': article.url,
                        'source': source_url,
                        'publish_date': str(article.publish_date) if article.publish_date else '',
                        'date': datetime.now().strftime('%Y-%m-%d')
                    })
                    
                except Exception as e:
                    continue
            
            print(f"  ✓ 找到 {len(news_items)} 条新闻")
            return news_items
            
        except Exception as e:
            print(f"  ✗ 爬取失败: {e}")
            return []
    
    def crawl_all_sources(self):
        """爬取所有新闻源"""
        print(f"\n{'='*60}")
        print(f"开始爬取 Newspaper4k 新闻源")
        print(f"{'='*60}")
        
        sources = self.news_sources.get(self.sector, [])
        
        for source_url in sources:
            news_items = self.crawl_source(source_url)
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
        output_file = os.path.join(output_dir, f'{self.sector}_newspaper_{date_str}.json')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 已保存到: {output_file}")
        print(f"📊 共保存: {len(self.results)} 条新闻")

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Newspaper4k 新闻提取器')
    parser.add_argument('--sector', required=True, choices=['healthcare', 'education'], 
                        help='板块: healthcare 或 education')
    parser.add_argument('--hours', type=int, default=24, help='时间范围（小时）')
    
    args = parser.parse_args()
    
    crawler = Newspaper4kCrawler(args.sector, args.hours)
    crawler.crawl_all_sources()
    crawler.save_results()



