#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Newspaper4k 测试脚本 - 整站爬取
"""

import newspaper
from newspaper import Config

print("=" * 60)
print("测试2：新浪财经整站爬取")
print("=" * 60)

# 配置
config = Config()
config.language = 'zh'
config.memoize_articles = False
config.fetch_images = False

try:
    # 构建新闻源
    print("\n📰 正在构建新闻源...")
    source = newspaper.build('https://finance.sina.com.cn/', config=config)
    
    print(f"✅ 发现文章数: {source.size()}")
    print(f"✅ 分类页面数: {len(source.category_urls())}")
    
    # 显示前10个文章URL
    print("\n📋 前10个文章URL:")
    for i, article in enumerate(source.articles[:10]):
        print(f"{i+1}. {article.url}")
    
    # 测试下载第一篇文章
    if source.articles:
        print("\n" + "=" * 60)
        print("测试下载第一篇文章")
        print("=" * 60)
        
        first_article = source.articles[0]
        first_article.download()
        first_article.parse()
        
        print(f"✅ 标题: {first_article.title}")
        print(f"✅ URL: {first_article.url}")
        print(f"✅ 正文长度: {len(first_article.text)} 字符")
        if first_article.text:
            print(f"✅ 正文预览: {first_article.text[:150]}...")
    
except Exception as e:
    print(f"❌ 错误: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("测试完成")
print("=" * 60)
