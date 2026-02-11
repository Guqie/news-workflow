#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将JSON格式的新闻数据转换为CSV格式
"""

import json
import csv
import sys
from datetime import datetime

def convert_json_to_csv(json_file, csv_file):
    """将JSON转换为CSV"""
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if not data:
        print("没有数据")
        return
    
    # 提取字段
    fieldnames = ['标题', '链接', '来源', '发布时间', '关键词', '采集日期']
    
    with open(csv_file, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for item in data:
            row = {
                '标题': item.get('title', ''),
                '链接': item.get('url', ''),
                '来源': item.get('source', ''),
                '发布时间': item.get('published', ''),
                '关键词': item.get('keyword', ''),
                '采集日期': datetime.now().strftime('%Y-%m-%d')
            }
            writer.writerow(row)
    
    print(f"✓ 已转换 {len(data)} 条新闻到 {csv_file}")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("用法: python convert_json_to_csv.py <输入JSON> <输出CSV>")
        sys.exit(1)
    
    convert_json_to_csv(sys.argv[1], sys.argv[2])
