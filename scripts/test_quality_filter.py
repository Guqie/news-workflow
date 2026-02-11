#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试质量筛选效果
"""

import json
import sys
sys.path.append('/root/clawd/news-workflow/scripts')
from keyword_filter import KeywordFilter
from quality_filter import QualityFilter

# 读取数据
with open('/root/clawd/news-workflow/data/raw/strategic_emerging_aggregated_20260211.json', 'r') as f:
    news_list = json.load(f)

print("="*70)
print("质量筛选测试")
print("="*70)
print(f"原始新闻数量: {len(news_list)}\n")

# 第一步：关键词筛选
print("第一步：关键词筛选")
print("-"*70)
keyword_filter = KeywordFilter()
filtered_by_keyword, kw_stats = keyword_filter.filter_news_list(news_list)

# 第二步：质量筛选
print("\n第二步：质量筛选")
print("-"*70)
quality_filter = QualityFilter()
final_news, quality_stats = quality_filter.filter_news_list(filtered_by_keyword)

# 显示总体结果
print("\n" + "="*70)
print("总体筛选结果")
print("="*70)
print(f"原始: {len(news_list)} 条")
print(f"关键词筛选后: {len(filtered_by_keyword)} 条")
print(f"质量筛选后: {len(final_news)} 条")
print(f"总筛选率: {(len(news_list) - len(final_news)) / len(news_list) * 100:.1f}%")

# 显示被质量筛选排除的示例
print("\n" + "="*70)
print("被质量筛选排除的新闻示例:")
print("="*70)
excluded_count = 0
for news in filtered_by_keyword:
    keep, reason = quality_filter.filter_news(news)
    if not keep and excluded_count < 10:
        print(f"\n{excluded_count+1}. {news['title'][:60]}...")
        print(f"   原因: {reason}")
        excluded_count += 1

print("\n测试完成！")
