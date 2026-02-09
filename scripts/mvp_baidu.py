#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MVP版本：使用百度新闻API
更简单、更稳定
"""

import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import json

def search_baidu_news(keyword, max_results=5):
    """
    从百度新闻搜索
    """
    print(f"\n🔍 正在搜索: {keyword}")
    print("-" * 60)
    
    url = "https://www.baidu.com/s"
    params = {
        "tn": "news",
        "word": keyword,
        "rtt": "1"  # 最新
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            print(f"❌ 请求失败: {response.status_code}")
            return []
        
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        
        # 查找新闻结果
        news_items = soup.find_all('div', class_='result')
        
        for i, item in enumerate(news_items[:max_results]):
            try:
                # 提取标题和链接
                title_tag = item.find('h3')
                if title_tag:
                    link_tag = title_tag.find('a')
                    if link_tag:
                        title = link_tag.get_text().strip()
                        link = link_tag.get('href', '')
                        
                        if title and link:
                            results.append({
                                'title': title,
                                'link': link
                            })
                            print(f"{i+1}. {title}")
                            print(f"   🔗 {link[:80]}...\n")
            except:
                continue
        
        return results
        
    except Exception as e:
        print(f"❌ 爬取失败: {e}")
        return []

def main():
    """
    主函数：快速测试
    """
    print("\n" + "="*60)
    print("📰 新闻爬虫 MVP - 百度新闻版")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # 测试关键词
    keywords = {
        "教育人才": ["教育政策", "人才引进"],
        "医疗健康": ["医疗政策", "生物医药"]
    }
    
    all_results = {}
    
    for sector, kw_list in keywords.items():
        print(f"\n📋 {sector}板块")
        print("="*60)
        all_results[sector] = []
        
        for keyword in kw_list:
            results = search_baidu_news(keyword, max_results=3)
            all_results[sector].extend(results)
            time.sleep(2)
    
    # 统计
    print("\n" + "="*60)
    print("📊 统计结果")
    print("="*60)
    for sector, results in all_results.items():
        print(f"{sector}: {len(results)} 条新闻")
    print("\n✅ MVP测试完成！")

if __name__ == '__main__':
    main()
