#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试优化后的配置 - 小规模检索测试
"""

import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def load_config():
    """加载优化后的配置"""
    with open('../references/config.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def test_keywords(sector_key, test_count=3):
    """测试关键词检索"""
    config = load_config()
    keywords = config['sectors'][sector_key]['keywords'][:test_count]
    sector_name = config['sectors'][sector_key]['name']
    
    print(f"\n{'='*60}")
    print(f"测试 {sector_name} - 前{test_count}个关键词")
    print(f"{'='*60}")
    
    results = []
    for keyword in keywords:
        try:
            search_url = f"https://news.google.com/rss/search?q={keyword}+when:1d&hl=zh-CN&gl=CN&ceid=CN:zh-Hans"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            
            response = requests.get(search_url, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'xml')
                items = soup.find_all('item')
                count = len(items[:5])
                
                print(f"✓ '{keyword}': 找到 {count} 条新闻")
                
                # 显示第一条新闻标题
                if items:
                    first_title = items[0].find('title')
                    if first_title:
                        print(f"  示例: {first_title.text[:50]}...")
                
                results.append({'keyword': keyword, 'count': count})
            else:
                print(f"✗ '{keyword}': HTTP {response.status_code}")
                
        except Exception as e:
            print(f"✗ '{keyword}': {str(e)}")
    
    total = sum(r['count'] for r in results)
    print(f"\n总计: {total} 条新闻")
    return results

if __name__ == '__main__':
    print("开始检索测试...")
    
    # 测试战略新兴产业
    test_keywords('strategic_emerging', 5)
    
    # 测试高科技产业
    test_keywords('hightech', 5)
    
    print("\n" + "="*60)
    print("检索测试完成")
    print("="*60)
