#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MVP版本：最简单的新闻爬虫
从中国搜索抓取24小时内的新闻
"""

import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

def search_chinaso(keyword, max_results=10):
    """
    从中国搜索获取新闻
    """
    print(f"\n🔍 正在搜索关键词: {keyword}")
    print("=" * 60)
    
    # 构造搜索URL
    url = "https://www.chinaso.com/search/pagesearch.htm"
    params = {
        "q": keyword,
        "time": "1",  # 24小时内
        "page": 1
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
        
        # 解析搜索结果（需要根据实际页面结构调整）
        # 这里先用通用方法提取链接和标题
        news_items = soup.find_all('a', href=True)
        
        count = 0
        for item in news_items:
            if count >= max_results:
                break
                
            title = item.get_text().strip()
            link = item.get('href', '')
            
            # 简单过滤
            if len(title) > 10 and 'http' in link:
                results.append({
                    'title': title,
                    'link': link
                })
                count += 1
        
        return results
        
    except Exception as e:
        print(f"❌ 爬取失败: {e}")
        return []

def main():
    """
    主函数：测试爬取教育和医疗新闻
    """
    print("\n" + "="*60)
    print("📰 新闻爬虫 MVP 测试")
    print(f"⏰ 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # 教育人才板块关键词
    education_keywords = ["教育政策", "人才引进"]
    
    # 医疗健康板块关键词
    healthcare_keywords = ["医疗政策", "生物医药"]
    
    print("\n📚 教育人才板块")
    print("-"*60)
    for keyword in education_keywords:
        results = search_chinaso(keyword, max_results=5)
        for i, news in enumerate(results, 1):
            print(f"{i}. {news['title']}")
            print(f"   🔗 {news['link']}\n")
        time.sleep(2)  # 避免请求过快
    
    
    print("\n🏥 医疗健康板块")
    print("-"*60)
    for keyword in healthcare_keywords:
        results = search_chinaso(keyword, max_results=5)
        for i, news in enumerate(results, 1):
            print(f"{i}. {news['title']}")
            print(f"   🔗 {news['link']}\n")
        time.sleep(2)  # 避免请求过快
    
    print("\n" + "="*60)
    print("✅ 测试完成！")
    print("="*60)

if __name__ == '__main__':
    main()
