#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试大模型筛选效果
"""

import json
import sys
sys.path.append('/root/clawd/news-workflow/scripts')
from keyword_filter import KeywordFilter
from quality_filter import QualityFilter
from llm_filter import LLMFilter

# 读取数据
with open('/root/clawd/news-workflow/data/raw/strategic_emerging_aggregated_20260211.json', 'r') as f:
    news_list = json.load(f)

print("="*70)
print("完整筛选流程测试")
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
filtered_by_quality, quality_stats = quality_filter.filter_news_list(filtered_by_keyword)

# 第三步：大模型筛选（全部337条）
print("\n第三步：大模型筛选（全部337条）")
print("-"*70)
llm_filter = LLMFilter()
final_news, llm_stats, llm_results = llm_filter.filter_all(filtered_by_quality)

# 显示总体结果
print("\n" + "="*70)
print("总体筛选结果（前10条测试）")
print("="*70)
print(f"原始: {len(news_list)} 条")
print(f"关键词筛选后: {len(filtered_by_keyword)} 条")
print(f"质量筛选后: {len(filtered_by_quality)} 条")
print(f"大模型筛选后: {len(final_news)} 条（测试前10条）")

# 显示大模型判断详情
print("\n" + "="*70)
print("大模型判断详情:")
print("="*70)
for result in llm_results:
    idx = result['id'] - 1
    news = filtered_by_quality[idx]
    status = "✅ 保留" if result['keep'] else "❌ 排除"
    print(f"\n{result['id']}. {status}")
    print(f"   标题: {news['title'][:60]}...")
    print(f"   原因: {result['reason']}")

print("\n测试完成！")
