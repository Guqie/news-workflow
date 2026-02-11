#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Newspaper4k 多网站测试
"""

import newspaper
from newspaper import Article, Config
import time

# 测试网站列表
test_sites = [
    {
        "name": "东方财富",
        "url": "https://www.eastmoney.com/",
        "article_url": None  # 待获取
    },
    {
        "name": "新浪财经",
        "url": "https://finance.sina.com.cn/",
        "article_url": "https://finance.sina.com.cn/blockchain/roll/2026-02-10/doc-inhmitai5492496.shtml"
    },
    {
        "name": "36氪",
        "url": "https://36kr.com/",
        "article_url": None
    },
]

print("=" * 70)
print("Newspaper4k 多网站兼容性测试")
print("=" * 70)

config = Config()
config.language = 'zh'
config.memoize_articles = False
config.fetch_images = False
config.request_timeout = 10

for site in test_sites:
    print(f"\n{'='*70}")
    print(f"测试网站: {site['name']} - {site['url']}")
    print('='*70)
    
    try:
        # 测试1: 构建新闻源
        print(f"\n📰 正在构建新闻源...")
        source = newspaper.build(site['url'], config=config)
        
        print(f"✅ 发现文章数: {source.size()}")
        print(f"✅ 分类页面数: {len(source.category_urls())}")
        
        # 显示前5个文章URL
        if source.articles:
            print(f"\n📋 前5个文章URL:")
            for i, article in enumerate(source.articles[:5]):
                print(f"  {i+1}. {article.url}")
            
            # 测试2: 下载第一篇文章
            print(f"\n📄 测试下载第一篇文章...")
            first_article = source.articles[0]
            first_article.download()
            first_article.parse()
            
            print(f"✅ 标题: {first_article.title[:50]}...")
            print(f"✅ 正文长度: {len(first_article.text)} 字符")
            
            if first_article.text:
                print(f"✅ 正文预览: {first_article.text[:100]}...")
        else:
            print("⚠️  未发现文章")
        
        print(f"\n✅ {site['name']} 测试通过")
        
    except Exception as e:
        print(f"❌ {site['name']} 测试失败: {e}")
    
    time.sleep(2)  # 避免请求过快

print("\n" + "=" * 70)
print("测试完成")
print("=" * 70)
