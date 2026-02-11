#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试用户提供的新闻源列表
"""

import newspaper
from newspaper import Config
import time

# 用户提供的新闻源列表
news_sources = [
    {
        "name": "中国搜索",
        "url": "https://www.chinaso.com/",
        "type": "搜索引擎"
    },
    {
        "name": "中国科技网滚动新闻",
        "url": "https://www.stdaily.com/web/gdxw/node_324_2.html",
        "type": "滚动新闻"
    },
    {
        "name": "中国西藏网即时新闻",
        "url": "http://www.tibet.cn/cn/Instant/",
        "type": "即时新闻"
    },
    {
        "name": "人民网要闻",
        "url": "https://cpc.people.com.cn/GB/64093/64387/index1.html",
        "type": "要闻"
    },
    {
        "name": "人民网滚动新闻",
        "url": "http://finance.people.com.cn/GB/70846/index.html",
        "type": "滚动新闻"
    },
    {
        "name": "新浪滚动新闻",
        "url": "https://news.sina.com.cn/roll/",
        "type": "滚动新闻"
    },
    {
        "name": "新浪新闻要闻",
        "url": "https://news.sina.com.cn/china/",
        "type": "要闻"
    },
    {
        "name": "上海市要闻动态",
        "url": "https://www.shanghai.gov.cn/nw4411/index.html",
        "type": "政府要闻"
    },
    {
        "name": "中国经济网即时新闻",
        "url": "http://www.ce.cn/cysc/newmain/yc/jsxw/",
        "type": "即时新闻"
    }
]

print("=" * 70)
print("新闻源兼容性测试")
print("=" * 70)

config = Config()
config.language = 'zh'
config.memoize_articles = False
config.fetch_images = False
config.request_timeout = 10

results = []

for i, source in enumerate(news_sources, 1):
    print(f"\n[{i}/{len(news_sources)}] 测试: {source['name']}")
    print(f"URL: {source['url']}")
    print(f"类型: {source['type']}")
    print("-" * 70)
    
    try:
        # 构建新闻源
        news_source = newspaper.build(source['url'], config=config)
        
        article_count = news_source.size()
        category_count = len(news_source.category_urls())
        
        result = {
            "name": source['name'],
            "url": source['url'],
            "type": source['type'],
            "articles": article_count,
            "categories": category_count,
            "status": "✅ 成功" if article_count > 0 else "⚠️ 无文章"
        }
        
        print(f"✅ 发现文章: {article_count}")
        print(f"✅ 分类页面: {category_count}")
        
        # 显示前3个文章URL
        if news_source.articles:
            print(f"📋 前3个文章URL:")
            for j, article in enumerate(news_source.articles[:3], 1):
                print(f"  {j}. {article.url}")
        
        results.append(result)
        
    except Exception as e:
        result = {
            "name": source['name'],
            "url": source['url'],
            "type": source['type'],
            "articles": 0,
            "categories": 0,
            "status": f"❌ 失败: {str(e)[:50]}"
        }
        print(f"❌ 错误: {e}")
        results.append(result)
    
    time.sleep(1)  # 避免请求过快

# 输出汇总
print("\n" + "=" * 70)
print("测试结果汇总")
print("=" * 70)

for result in results:
    print(f"\n{result['status']} {result['name']}")
    print(f"  文章数: {result['articles']}, 分类数: {result['categories']}")

print("\n" + "=" * 70)
print("测试完成")
print("=" * 70)
