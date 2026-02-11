#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将JSON新闻数据转换为CSV格式
"""

import json
import csv
import sys
from datetime import datetime

def json_to_csv(json_file, csv_file):
    """将JSON转换为CSV"""
    
    # 读取JSON
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if not data:
        print("⚠️  JSON文件为空")
        return
    
    # CSV字段
    fieldnames = ['标题', '链接', '来源', '发布时间', '关键词', '采集日期']
    
    # 写入CSV
    with open(csv_file, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for item in data:
            writer.writerow({
                '标题': item.get('title', ''),
                '链接': item.get('url', ''),
                '来源': item.get('source', ''),
                '发布时间': item.get('publish_date', ''),
                '关键词': item.get('keyword', ''),
                '采集日期': item.get('date', '')
            })
    
    print(f"✅ 转换完成: {csv_file}")
    print(f"📊 共 {len(data)} 条新闻")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("用法: python3 json_to_csv.py <input.json> <output.csv>")
        sys.exit(1)
    
    json_to_csv(sys.argv[1], sys.argv[2])
