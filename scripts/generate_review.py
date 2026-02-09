#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成审核报告
将编辑后的新闻整理成易于审核的格式
"""

import argparse
import json
import os
from datetime import datetime

def generate_review(date_str):
    """生成指定日期的审核报告"""
    
    # 读取教育人才板块
    edu_file = f"../data/edited/education_{date_str}.json"
    health_file = f"../data/edited/healthcare_{date_str}.json"
    
    report = []
    report.append("# 新闻审核报告")
    report.append(f"\n**日期：** {date_str}")
    report.append(f"\n**生成时间：** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("\n---\n")
    
    # 处理教育人才板块
    if os.path.exists(edu_file):
        with open(edu_file, 'r', encoding='utf-8') as f:
            edu_news = json.load(f)
        
        report.append("## 一、教育人才板块\n")
        report.append(f"**数量：** {len(edu_news)} 条\n")
        
        for i, news in enumerate(edu_news, 1):
            report.append(f"\n### {i}. {news['title']}\n")
            report.append(f"- **关键词：** {', '.join(news['keywords'])}")
            report.append(f"- **来源：** {news['source']}")
            report.append(f"- **摘要：** {news['summary']}\n")
    
    report.append("\n---\n")
    
    # 处理医疗健康板块
    if os.path.exists(health_file):
        with open(health_file, 'r', encoding='utf-8') as f:
            health_news = json.load(f)
        
        report.append("## 二、医疗健康板块\n")
        report.append(f"**数量：** {len(health_news)} 条\n")
        
        for i, news in enumerate(health_news, 1):
            report.append(f"\n### {i}. {news['title']}\n")
            report.append(f"- **关键词：** {', '.join(news['keywords'])}")
            report.append(f"- **来源：** {news['source']}")
            report.append(f"- **摘要：** {news['summary']}\n")
    
    # 保存报告
    output_file = f"../data/review_{date_str}.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))
    
    print(f"✓ 审核报告已生成: {output_file}")

def main():
    parser = argparse.ArgumentParser(description='生成审核报告')
    parser.add_argument('--date', required=True, help='日期 YYYYMMDD')
    args = parser.parse_args()
    
    generate_review(args.date)

if __name__ == '__main__':
    main()
