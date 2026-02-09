#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新闻数据导出工具 - 将 JSON 转换为 CSV
"""

import json
import csv
import sys

def export_to_csv(json_file, csv_file):
    """将 JSON 新闻数据导出为 CSV"""
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    with open(csv_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['title', 'source', 'published_date', 'url', 'keyword', 'date'])
        writer.writeheader()
        writer.writerows(data)
    
    print(f"✅ 已导出 {len(data)} 条新闻到 {csv_file}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("用法: python3 export_to_csv.py <输入JSON文件> <输出CSV文件>")
        sys.exit(1)
    
    export_to_csv(sys.argv[1], sys.argv[2])
