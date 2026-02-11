#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速获取今天的战略新兴产业和高科技产业新闻
"""

import json
import csv
import os
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import time

class QuickNewsFetcher:
    def __init__(self):
        self.config = self.load_config()
        self.results = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
    def load_config(self):
        """加载配置文件"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(script_dir, '../references/config.json')
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def search_google_news(self, keyword, sector_name):
        """搜索Google News"""
        try:
            # 使用Google News搜索
            search_url = f"https://news.google.com/rss/search?q={keyword}+when:1d&hl=zh-CN&gl=CN&ceid=CN:zh-Hans"
            
            response = requests.get(search_url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'xml')
                items = soup.find_all('item')
                
                count = 0
                for item in items[:5]:  # 每个关键词取前5条（增加到5条）
                    title = item.find('title')
                    link = item.find('link')
                    pub_date = item.find('pubDate')
                    source = item.find('source')
                    
                    if title and link:
                        self.results.append({
                            '标题': title.text,
                            '链接': link.text,
                            '来源': source.text if source else '',
                            '发布时间': pub_date.text if pub_date else '',
                            '关键词': keyword,
                            '板块': sector_name,
                            '采集日期': datetime.now().strftime('%Y-%m-%d')
                        })
                        count += 1
                
                if count > 0:
                    print(f"  ✓ '{keyword}' 获取了 {count} 条新闻")
                return count
            else:
                print(f"  ✗ '{keyword}' 搜索失败: HTTP {response.status_code}")
                return 0
                
        except Exception as e:
            print(f"  ✗ '{keyword}' 搜索出错: {str(e)}")
            return 0
    
    def fetch_sector_news(self, sector_key, sector_name):
        """获取某个领域的新闻"""
        print(f"\n{'='*60}")
        print(f"开始获取{sector_name}新闻...")
        print(f"{'='*60}")
        
        keywords = self.config['sectors'][sector_key]['keywords']
        
        # 使用更多关键词（前15个）
        core_keywords = keywords[:15]
        
        total = 0
        for keyword in core_keywords:
            count = self.search_google_news(keyword, sector_name)
            total += count
            time.sleep(0.5)  # 避免请求过快
        
        print(f"\n{sector_name}共获取 {total} 条新闻")
        return total
    
    def fetch_all_news(self):
        """获取所有领域的新闻"""
        # 战略新兴产业
        self.fetch_sector_news('strategic_emerging', '战略新兴产业')
        
        # 高科技产业
        self.fetch_sector_news('hightech', '高科技产业')
        
        print(f"\n{'='*60}")
        print(f"总共获取了 {len(self.results)} 条新闻")
        print(f"{'='*60}")
        return self.results
    
    def save_to_csv(self, filename=None):
        """保存为CSV文件"""
        if not filename:
            today = datetime.now().strftime('%Y%m%d')
            filename = f'news_{today}_full.csv'
        
        # 确保data目录存在
        data_dir = os.path.join(os.path.dirname(__file__), '../data/raw')
        os.makedirs(data_dir, exist_ok=True)
        
        filepath = os.path.join(data_dir, filename)
        
        if self.results:
            with open(filepath, 'w', encoding='utf-8-sig', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=self.results[0].keys())
                writer.writeheader()
                writer.writerows(self.results)
            
            print(f"\n✓ 新闻已保存到: {filepath}")
        else:
            print(f"\n✗ 没有新闻数据，未创建CSV文件")
            filepath = None
        
        return filepath

if __name__ == '__main__':
    fetcher = QuickNewsFetcher()
    fetcher.fetch_all_news()
    csv_path = fetcher.save_to_csv()
