#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Newspaper4k 测试脚本 - 使用真实URL
"""

import newspaper
from newspaper import Article

print("=" * 60)
print("测试3：使用真实新闻URL")
print("=" * 60)

# 使用刚才获取到的真实URL
test_urls = [
    "https://finance.sina.com.cn/blockchain/roll/2026-02-10/doc-inhmitai5492496.shtml",
    "https://finance.sina.com.cn/blockchain/roll/2026-02-10/doc-inhmitaf8383965.shtml",
]

for i, url in enumerate(test_urls, 1):
    print(f"\n{'='*60}")
    print(f"测试文章 {i}: {url}")
    print('='*60)
    
    try:
        article = Article(url, language='zh')
        article.download()
        article.parse()
        
        print(f"✅ 标题: {article.title}")
        print(f"✅ 发布时间: {article.publish_date}")
        print(f"✅ 作者: {article.authors}")
        print(f"✅ 正文长度: {len(article.text)} 字符")
        
        if article.text:
            print(f"✅ 正文预览:\n{article.text[:200]}...")
        
        # 测试NLP功能
        if article.text:
            article.nlp()
            print(f"✅ 关键词: {article.keywords[:5]}")
            print(f"✅ 摘要长度: {len(article.summary)} 字符")
        
        break  # 成功一个就够了
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        continue

print("\n" + "=" * 60)
print("测试完成")
print("=" * 60)
