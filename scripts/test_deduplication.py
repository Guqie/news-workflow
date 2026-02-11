#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试去重效果
"""

import json
import sys
sys.path.append('/root/clawd/news-workflow/scripts')
from deduplicator import NewsDeduplicator

# 读取今天的新闻数据
print("读取新闻数据...")
with open('/root/clawd/news-workflow/data/raw/strategic_emerging_aggregated_20260211.json', 'r') as f:
    news_list = json.load(f)

print(f"原始新闻数量: {len(news_list)}\n")

# 创建去重器
deduplicator = NewsDeduplicator(similarity_threshold=0.8)

# 去重前显示一些标题
print("="*70)
print("去重前的部分标题（前10条）:")
print("="*70)
for i, news in enumerate(news_list[:10]):
    print(f"{i+1}. {news['title'][:60]}...")

print("\n开始去重...\n")

# 执行去重
unique_news = deduplicator.deduplicate(news_list)

print("\n" + "="*70)
print("去重结果统计:")
print("="*70)
print(f"原始数量: {len(news_list)}")
print(f"去重后数量: {len(unique_news)}")
print(f"移除数量: {len(news_list) - len(unique_news)}")
print(f"去重率: {(len(news_list) - len(unique_news)) / len(news_list) * 100:.1f}%")

# 找出一些相似标题的例子
print("\n" + "="*70)
print("相似标题示例（展示被去重的案例）:")
print("="*70)

found_examples = 0
for i, news1 in enumerate(news_list[:100]):  # 只检查前100条
    if found_examples >= 5:  # 最多显示5个例子
        break
    for news2 in news_list[i+1:100]:
        similarity = deduplicator.calculate_similarity(news1['title'], news2['title'])
        if 0.8 <= similarity < 1.0:  # 相似但不完全相同
            print(f"\n相似度: {similarity:.2%}")
            print(f"标题1: {news1['title']}")
            print(f"标题2: {news2['title']}")
            found_examples += 1
            break

print("\n测试完成！")
