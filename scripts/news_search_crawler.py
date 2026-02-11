#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新闻搜索爬虫 - 从新闻聚合网站搜索新闻
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
import os

class NewsSearchCrawler:
    """新闻搜索爬虫"""
    
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
    
    def load_config(self):
        """加载配置文件"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(script_dir, '../references/config.json')
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def search_baidu_news(self, keyword, max_results=10):
        """
        搜索百度新闻
        
        参数:
            keyword: 搜索关键词
            max_results: 最大结果数
        """
        print(f"\n🔍 搜索百度新闻: {keyword}")
        
        # 百度新闻搜索 URL
        search_url = f"https://www.baidu.com/s?tn=news&word={keyword}"
        
        try:
            response = self.session.get(search_url, timeout=10)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找新闻结果
            news_items = []
            results = soup.find_all('div', class_='result')
            
            for result in results[:max_results]:
                # 提取标题
                title_tag = result.find('h3')
                if not title_tag:
                    continue
                
                title = title_tag.get_text().strip()
                
                # 提取链接
                link_tag = title_tag.find('a')
                url = link_tag.get('href', '') if link_tag else ''
                
                # 提取来源和时间
                source_tag = result.find('span', class_='c-color-gray2')
                source = source_tag.get_text().strip() if source_tag else '未知来源'
                
                news_items.append({
                    'title': title,
                    'url': url,
                    'source': source,
                    'keyword': keyword,
                    'date': datetime.now().strftime('%Y-%m-%d')
                })
            
            print(f"  ✓ 找到 {len(news_items)} 条新闻")
            return news_items
            
        except Exception as e:
            print(f"  ✗ 搜索失败: {e}")
            return []
    
    def search_sogou_news(self, keyword, max_results=10):
        """
        搜索搜狗新闻
        
        参数:
            keyword: 搜索关键词
            max_results: 最大结果数
        """
        print(f"\n🔍 搜索搜狗新闻: {keyword}")
        
        # 搜狗新闻搜索 URL
        search_url = f"https://news.sogou.com/news?query={keyword}"
        
        try:
            response = self.session.get(search_url, timeout=10)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找新闻结果
            news_items = []
            results = soup.find_all('div', class_='news-box')
            
            for result in results[:max_results]:
                # 提取标题
                title_tag = result.find('h3')
                if not title_tag:
                    continue
                
                title = title_tag.get_text().strip()
                
                # 提取链接
                link_tag = title_tag.find('a')
                url = link_tag.get('href', '') if link_tag else ''
                
                # 提取来源
                source_tag = result.find('span', class_='news-from')
                source = source_tag.get_text().strip() if source_tag else '未知来源'
                
                news_items.append({
                    'title': title,
                    'url': url,
                    'source': source,
                    'keyword': keyword,
                    'date': datetime.now().strftime('%Y-%m-%d')
                })
            
            print(f"  ✓ 找到 {len(news_items)} 条新闻")
            return news_items
            
        except Exception as e:
            print(f"  ✗ 搜索失败: {e}")
            return []
    
    def search_with_keywords(self, keywords, max_results_per_keyword=10):
        """
        使用多个关键词搜索
        
        参数:
            keywords: 关键词列表
            max_results_per_keyword: 每个关键词的最大结果数
        """
        print(f"\n{'='*60}")
        print(f"开始搜索 - {self.config['sectors'][self.sector]['name']}")
        print(f"{'='*60}")
        
        for keyword in keywords:
            # 搜索百度新闻
            baidu_results = self.search_baidu_news(keyword, max_results_per_keyword)
            self.results.extend(baidu_results)
            
            time.sleep(2)  # 礼貌延迟
            
            # 搜索搜狗新闻
            sogou_results = self.search_sogou_news(keyword, max_results_per_keyword)
            self.results.extend(sogou_results)
            
            time.sleep(2)  # 礼貌延迟
        
        # 去重
        self.deduplicate()
    
    def deduplicate(self):
        """去重功能"""
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
        output_file = os.path.join(output_dir, f'{self.sector}_search_{date_str}.json')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 已保存到: {output_file}")
        print(f"📊 共保存: {len(self.results)} 条新闻")

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='新闻搜索爬虫')
    parser.add_argument('--sector', required=True, 
                        choices=['healthcare', 'education', 'strategic_emerging', 'hightech'], 
                        help='板块: healthcare, education, strategic_emerging, hightech')
    parser.add_argument('--keywords', nargs='+', help='搜索关键词列表')
    parser.add_argument('--count', type=int, default=10, help='每个关键词的最大结果数')
    
    args = parser.parse_args()
    
    crawler = NewsSearchCrawler(args.sector)
    
    # 如果没有指定关键词，使用默认的第一优先级关键词
    if not args.keywords:
        if args.sector == 'healthcare':
            keywords = ["医药产业 发展", "生物医药 创新", "医疗健康 政策", "医保 改革"]
        elif args.sector == 'education':
            keywords = ["人才政策 发展", "教育改革 创新", "人才培养 产业", "职业教育 发展"]
        elif args.sector == 'strategic_emerging':
            keywords = ["战略新兴产业", "新能源 发展", "新材料 产业", "数字经济"]
        elif args.sector == 'hightech':
            keywords = ["高科技产业", "人工智能 发展", "芯片 产业", "半导体"]
    else:
        keywords = args.keywords
    
    crawler.search_with_keywords(keywords, args.count)
    crawler.save_results()
