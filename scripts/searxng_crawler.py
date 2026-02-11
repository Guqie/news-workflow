#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SearXNG元搜索引擎爬虫
"""

import requests
import json
import os
from datetime import datetime
from typing import List, Dict

class SearXNGCrawler:
    """SearXNG元搜索引擎爬虫"""
    
    def __init__(self, sector, proxy=None):
        self.sector = sector
        self.config = self.load_config()
        self.results = []
        
        # SearXNG公共实例列表（按优先级）
        self.instances = [
            "https://searx.be",
            "https://searx.work",
            "https://search.bus-hit.me",
            "https://searx.tiekoetter.com",
            "https://searx.fmac.xyz",
            "https://search.sapti.me",
            "https://searx.prvcy.eu"
        ]
        self.current_instance = self.instances[0]
        self.timeout = 10
        
        # 代理配置
        self.proxies = None
        if proxy:
            self.proxies = {
                "http": proxy,
                "https": proxy
            }
            print(f"✓ 使用代理: {proxy}")
    
    def load_config(self):
        """加载配置文件"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(script_dir, '../references/config.json')
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def search_news(self, keyword: str, time_range: str = "day") -> List[Dict]:
        """
        搜索新闻
        
        参数:
            keyword: 搜索关键词
            time_range: 时间范围 (day/week/month/year)
        
        返回:
            新闻列表
        """
        print(f"\n🔍 搜索 SearXNG: {keyword}")
        
        params = {
            "q": keyword,
            "categories": "news",
            "format": "json",
            "time_range": time_range,
            "language": "zh-CN"
        }
        
        # 尝试多个实例
        for instance in self.instances:
            try:
                print(f"  尝试实例: {instance}")
                response = requests.get(
                    f"{instance}/search",
                    params=params,
                    timeout=self.timeout,
                    proxies=self.proxies
                )
                
                print(f"  状态码: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    results = data.get("results", [])
                    
                    print(f"  原始结果数: {len(results)}")
                    
                    # 如果结果为空，尝试下一个实例
                    if not results:
                        print(f"  ⚠️  实例 {instance} 返回空结果，尝试下一个")
                        continue
                    
                    # 转换为统一格式
                    news_items = []
                    for item in results:
                        news_items.append({
                            "title": item.get("title", ""),
                            "url": item.get("url", ""),
                            "content": item.get("content", ""),
                            "source": item.get("engine", "未知来源"),
                            "publish_date": item.get("publishedDate", ""),
                            "keyword": keyword,
                            "date": datetime.now().strftime('%Y-%m-%d')
                        })
                    
                    print(f"  ✓ 找到 {len(news_items)} 条新闻 (实例: {instance})")
                    return news_items
                else:
                    print(f"  ⚠️  实例 {instance} 返回状态码: {response.status_code}")
                    
            except Exception as e:
                print(f"  ⚠️  实例 {instance} 失败: {e}")
                continue
        
        print(f"  ✗ 所有实例都失败")
        return []
    
    def search_with_keywords(self, keywords: List[str], time_range: str = "day"):
        """使用多个关键词搜索"""
        print(f"\n{'='*60}")
        print(f"开始搜索 SearXNG - {self.config['sectors'][self.sector]['name']}")
        print(f"时间范围: {time_range}")
        print(f"{'='*60}")
        
        for keyword in keywords:
            news_items = self.search_news(keyword, time_range)
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
        output_file = os.path.join(output_dir, f'{self.sector}_searxng_{date_str}.json')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 已保存到: {output_file}")
        print(f"📊 共保存: {len(self.results)} 条新闻")
        
        # 打印前5条标题
        print(f"\n📰 前5条新闻标题：")
        for i, news in enumerate(self.results[:5], 1):
            print(f"{i}. {news['title']}")
            print(f"   来源: {news['source']} | 发布: {news['publish_date']}")

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='SearXNG元搜索引擎爬虫')
    parser.add_argument('--sector', required=True, 
                        choices=['healthcare', 'education', 'strategic_emerging', 'hightech'], 
                        help='板块')
    parser.add_argument('--keywords', nargs='+', help='搜索关键词列表')
    parser.add_argument('--time-range', default='day', 
                        choices=['day', 'week', 'month', 'year'],
                        help='时间范围')
    parser.add_argument('--proxy', help='代理地址，格式: http://host:port 或 socks5://host:port')
    
    args = parser.parse_args()
    
    crawler = SearXNGCrawler(args.sector, proxy=args.proxy)
    
    # 如果没有指定关键词，使用默认关键词
    if not args.keywords:
        if args.sector == 'strategic_emerging':
            keywords = ["战略新兴产业", "新能源", "新材料"]
        elif args.sector == 'hightech':
            keywords = ["高科技产业", "人工智能", "芯片"]
        elif args.sector == 'healthcare':
            keywords = ["医药产业", "生物医药"]
        else:
            keywords = ["人才政策", "教育改革"]
    else:
        keywords = args.keywords
    
    crawler.search_with_keywords(keywords, args.time_range)
    crawler.save_results()
