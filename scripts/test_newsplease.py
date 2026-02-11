#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
News-please 功能测试
"""

from newsplease import NewsPlease
import time

print("=" * 70)
print("News-please 功能测试")
print("=" * 70)

# 测试URL列表
test_urls = [
    "https://finance.sina.com.cn/blockchain/roll/2026-02-10/doc-inhmitai5492496.shtml",
    "https://cpc.people.com.cn/n1/2026/0210/c64094-40378901.html",
]

for i, url in enumerate(test_urls, 1):
    print(f"\n{'='*70}")
    print(f"测试 {i}: {url}")
    print('='*70)
    
    try:
        print("📡 提取文章...")
        article = NewsPlease.from_url(url)
        
        print(f"✅ 标题: {article.title}")
        print(f"✅ 作者: {article.authors}")
        print(f"✅ 发布时间: {article.date_publish}")
        print(f"✅ 语言: {article.language}")
        print(f"✅ 正文长度: {len(article.maintext) if article.maintext else 0} 字符")
        
        if article.maintext:
            print(f"✅ 正文预览:\n{article.maintext[:200]}...")
        
        print(f"\n✅ 测试成功")
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
    
    time.sleep(1)

print("\n" + "=" * 70)
print("测试完成")
print("=" * 70)
