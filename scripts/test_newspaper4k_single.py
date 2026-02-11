#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Newspaper4k 测试脚本 - 单篇文章提取
"""

import newspaper
from newspaper import Article

# 测试1：新浪财经文章
print("=" * 60)
print("测试1：新浪财经文章提取")
print("=" * 60)

url1 = "https://finance.sina.com.cn/china/gncj/2024-02-10/doc-inaaiyhw8765432.shtml"

try:
    article = Article(url1, language='zh')
    article.download()
    article.parse()
    
    print(f"✅ 标题: {article.title}")
    print(f"✅ 作者: {article.authors}")
    print(f"✅ 发布时间: {article.publish_date}")
    print(f"✅ 正文长度: {len(article.text)} 字符")
    print(f"✅ 主图: {article.top_image}")
    print(f"✅ 正文预览: {article.text[:200]}...")
    
except Exception as e:
    print(f"❌ 错误: {e}")

print("\n" + "=" * 60)
print("测试完成")
print("=" * 60)
