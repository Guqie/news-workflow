#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新闻报告生成器
"""

import json
from datetime import datetime
from collections import Counter

def generate_report(date_str):
    """生成新闻报告"""
    report = []
    report.append("=" * 60)
    report.append(f"新闻收集日报 - {date_str}")
    report.append("=" * 60)
    report.append("")
    
    # 医疗健康板块
    report.append("## 一、医疗健康板块")
    report.append("")
    
    sectors = {
        'healthcare': '医疗健康',
        'education': '教育人才'
    }
    
    for sector_key, sector_name in sectors.items():
        report.append(f"### {sector_name}板块")
        report.append("")
        
        total = 0
        sources = ['google', 'rss', 'rolling']
        
        for source in sources:
            file_path = f'../data/raw/{sector_key}_{source}_{date_str}.json'
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    count = len(data)
                    total += count
                    source_name = {'google': 'Google新闻', 'rss': 'RSS新闻', 'rolling': '滚动新闻'}[source]
                    report.append(f"- {source_name}: {count}条")
            except:
                pass
        
        report.append(f"- **小计**: {total}条")
        report.append("")
    
    return "\n".join(report)

if __name__ == '__main__':
    date_str = datetime.now().strftime('%Y%m%d')
    report = generate_report(date_str)
    
    # 保存报告
    output_file = f'../data/raw/news_report_{date_str}.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(report)
    print(f"\n✅ 报告已保存到: {output_file}")
