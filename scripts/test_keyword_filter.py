#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试关键词筛选效果
"""

import json
import sys
sys.path.append('/root/clawd/news-workflow/scripts')
from keyword_filter import KeywordFilter

# 读取今天的新闻数据
print("读取新闻数据...")
with open('/root/clawd/news-workflow/data/raw/strategic_emerging_aggregated_20260211.json', 'r') as f:
    news_list = json.load(f)

print(f"原始新闻数量: {len(news_list)}\n")

# 创建关键词筛选器
keyword_filter = KeywordFilter()

print("="*70)
print("开始关键词筛选...")
print("="*70)

# 执行筛选
filtered_news, stats = keyword_filter.filter_news_list(news_list)

# 显示筛选率
print(f"\n筛选率: {(stats['total'] - stats['kept']) / stats['total'] * 100:.1f}%")

# 显示保留的新闻示例
print("\n" + "="*70)
print("保留的新闻示例（前10条）:")
print("="*70)
for i, news in enumerate(filtered_news[:10]):
    keep, reason = keyword_filter.filter_news(news)
    print(f"{i+1}. {news['title'][:60]}...")
    print(f"   原因: {reason}")

# 显示被排除的新闻示例
print("\n" + "="*70)
print("被排除的新闻示例:")
print("="*70)
excluded_count = 0
for news in news_list:
    keep, reason = keyword_filter.filter_news(news)
    if not keep and excluded_count < 10:
        print(f"\n标题: {news['title'][:60]}...")
        print(f"原因: {reason}")
        excluded_count += 1

print("\n测试完成！")
