#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国搜索关键词搜索测试 - 轻量级版本（requests + BeautifulSoup）
"""

import requests
from bs4 import BeautifulSoup
import urllib.parse
import time

def test_chinaso_search_simple(keyword):
    """使用requests测试中国搜索"""
    
    print(f"\n{'='*70}")
    print(f"测试关键词: {keyword}")
    print('='*70)
    
    try:
        # 构建搜索URL
        base_url = "https://www.chinaso.com/search/pagesearch.htm"
        params = {
            'q': keyword,
            'page': 1
        }
        
        search_url = f"{base_url}?{urllib.parse.urlencode(params)}"
        print(f"🔍 搜索URL: {search_url}")
        
        # 发送请求
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        print("📡 发送请求...")
        response = requests.get(search_url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        
        print(f"✅ 状态码: {response.status_code}")
        
        if response.status_code == 200:
            # 解析HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 尝试多种选择器
            selectors = [
                'div.news-item',
                'div.result',
                'div.item',
                'div[class*="result"]',
                'a[href*="http"]'
            ]
            
            results = []
            for selector in selectors:
                elements = soup.select(selector)
                if elements:
                    print(f"✅ 使用选择器: {selector}, 找到 {len(elements)} 个元素")
                    results = elements
                    break
            
            if results:
                print(f"\n📊 搜索结果数量: {len(results)}")
                print(f"\n前5个结果:")
                
                for i, result in enumerate(results[:5], 1):
                    try:
                        # 提取标题和链接
                        title = result.get_text(strip=True)[:80]
                        link = result.get('href', '')
                        
                        if title:
                            print(f"\n{i}. {title}")
                        if link:
                            print(f"   链接: {link}")
                    except:
                        continue
                
                return len(results)
            else:
                print("⚠️  未找到搜索结果")
                print("\n📄 页面内容片段:")
                print(response.text[:500])
                return 0
        else:
            print(f"❌ 请求失败: {response.status_code}")
            return 0
            
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return 0

if __name__ == '__main__':
    # 测试关键词
    test_keywords = [
        "战略新兴产业",
        "新能源",
        "人工智能"
    ]
    
    print("=" * 70)
    print("中国搜索关键词搜索测试（轻量级版本）")
    print("=" * 70)
    
    results_summary = []
    
    for keyword in test_keywords:
        count = test_chinaso_search_simple(keyword)
        results_summary.append({
            'keyword': keyword,
            'count': count
        })
        time.sleep(2)
    
    # 输出汇总
    print("\n" + "=" * 70)
    print("测试结果汇总")
    print("=" * 70)
    
    for result in results_summary:
        status = "✅" if result['count'] > 0 else "❌"
        print(f"{status} {result['keyword']}: {result['count']} 个结果")
    
    print("\n" + "=" * 70)
    print("测试完成")
    print("=" * 70)
