#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
导出筛选结果为CSV格式
"""

import json
import csv
import sys
sys.path.append('/root/clawd/news-workflow/scripts')
from keyword_filter import KeywordFilter
from quality_filter import QualityFilter
from llm_filter import LLMFilter

# 读取数据
with open('/root/clawd/news-workflow/data/raw/strategic_emerging_aggregated_20260211.json', 'r') as f:
    news_list = json.load(f)

print("开始完整筛选流程...")
print(f"原始新闻数量: {len(news_list)}\n")

# 第一步：关键词筛选
print("第一步：关键词筛选")
keyword_filter = KeywordFilter()
filtered_by_keyword, _ = keyword_filter.filter_news_list(news_list)

# 第二步：质量筛选
print("\n第二步：质量筛选")
quality_filter = QualityFilter()
filtered_by_quality, _ = quality_filter.filter_news_list(filtered_by_keyword)

# 第三步：大模型筛选
print("\n第三步：大模型筛选")
llm_filter = LLMFilter()
final_news, stats, results = llm_filter.filter_all(filtered_by_quality)

# 导出CSV
output_file = '/root/clawd/news-workflow/data/filtered/strategic_emerging_filtered_20260211.csv'
print(f"\n导出CSV到: {output_file}")

# 确保目录存在
import os
os.makedirs(os.path.dirname(output_file), exist_ok=True)

with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(['标题', '来源', '链接', '发布时间'])
    
    for news in final_news:
        writer.writerow([
            news.get('title', ''),
            news.get('source', ''),
            news.get('link', ''),
            news.get('pubDate', '')
        ])

print(f"\n导出完成！共 {len(final_news)} 条新闻")
print(f"文件路径: {output_file}")
