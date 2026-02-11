#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统计被删除新闻的原因
"""

import json
import sys
sys.path.append('/root/clawd/news-workflow/scripts')
from keyword_filter import KeywordFilter

# 读取数据
with open('/root/clawd/news-workflow/data/raw/strategic_emerging_aggregated_20260211.json', 'r') as f:
    news_list = json.load(f)

keyword_filter = KeywordFilter()

# 统计排除原因
excluded_by_reason = {
    '股票类': [],
    '排除领域': [],
    '未匹配关键词': []
}

for news in news_list:
    keep, reason = keyword_filter.filter_news(news)
    if not keep:
        if '排除关键词' in reason:
            excluded_by_reason['股票类'].append((news['title'], reason))
        elif '排除领域' in reason:
            excluded_by_reason['排除领域'].append((news['title'], reason))
        else:
            excluded_by_reason['未匹配关键词'].append((news['title'], reason))

print("="*70)
print("被删除新闻原因统计")
print("="*70)

# 显示统计结果
print(f"\n总计被删除: {len(news_list) - sum(1 for n in news_list if keyword_filter.filter_news(n)[0])}")
print(f"1. 股票类: {len(excluded_by_reason['股票类'])} 条")
print(f"2. 排除领域: {len(excluded_by_reason['排除领域'])} 条")
print(f"3. 未匹配关键词: {len(excluded_by_reason['未匹配关键词'])} 条")

# 显示股票类示例
print("\n" + "="*70)
print("1. 股票类新闻示例（前10条）:")
print("="*70)
for i, (title, reason) in enumerate(excluded_by_reason['股票类'][:10]):
    print(f"{i+1}. {title[:60]}...")
    print(f"   {reason}")

# 显示排除领域示例
print("\n" + "="*70)
print("2. 排除领域新闻示例（前10条）:")
print("="*70)
for i, (title, reason) in enumerate(excluded_by_reason['排除领域'][:10]):
    print(f"{i+1}. {title[:60]}...")
    print(f"   {reason}")

# 显示未匹配关键词示例
print("\n" + "="*70)
print("3. 未匹配关键词新闻示例（前20条）:")
print("="*70)
for i, (title, reason) in enumerate(excluded_by_reason['未匹配关键词'][:20]):
    print(f"{i+1}. {title[:60]}...")

print("\n统计完成！")
