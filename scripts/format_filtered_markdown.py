#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成筛选后的高质量新闻markdown报告
"""

import json
from datetime import datetime
from pathlib import Path

def format_news_item(item, index, sector_name):
    """格式化单条新闻"""
    title = item.get('title', '无标题')
    source = item.get('source', '未知来源')
    url = item.get('url', '#')
    published = item.get('published', '未知时间')
    summary = item.get('summary', item.get('description', ''))
    score = item.get('quality_score', 0)
    
    # 格式化输出
    output = f"""
## {index}. {title}

**标题：** {title}

**来源：** {source}

**所属类别：** {sector_name}

**关键词：** 待提取

**发布时间：** {published}

**链接：** {url}

**质量评分：** {score}分

**摘要：**
{summary if summary else '暂无摘要'}

---

"""
    return output

def main():
    # 数据文件路径
    data_dir = Path(__file__).parent.parent / "data" / "raw"
    date_str = datetime.now().strftime("%Y%m%d")
    
    report = []
    
    # 添加报告头部
    report.append(f"# 每日新闻资讯汇总（高质量筛选版）\n")
    report.append(f"**生成时间：** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    report.append(f"**日期：** {datetime.now().strftime('%Y年%m月%d日')}\n")
    report.append("\n---\n")
    
    # 医疗健康板块
    healthcare_file = data_dir / f"healthcare_filtered_{date_str}.json"
    if healthcare_file.exists():
        with open(healthcare_file, 'r', encoding='utf-8') as f:
            healthcare_data = json.load(f)
        
        report.append("\n# 🏥 医疗健康板块\n")
        report.append(f"\n**共筛选出 {len(healthcare_data)} 条高质量新闻**\n")
        
        for idx, item in enumerate(healthcare_data, 1):
            report.append(format_news_item(item, idx, "医疗健康"))
    
    # 教育人才板块
    education_file = data_dir / f"education_filtered_{date_str}.json"
    if education_file.exists():
        with open(education_file, 'r', encoding='utf-8') as f:
            education_data = json.load(f)
        
        report.append("\n# 🎓 教育人才板块\n")
        report.append(f"\n**共筛选出 {len(education_data)} 条高质量新闻**\n")
        
        for idx, item in enumerate(education_data, 1):
            report.append(format_news_item(item, idx, "教育人才"))
    
    # 保存报告
    output_file = data_dir / f"daily_news_filtered_{date_str}.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("".join(report))
    
    print(f"✅ 高质量新闻报告已生成：{output_file}")
    print(f"📊 文件大小：{output_file.stat().st_size / 1024:.2f} KB")
    
    return str(output_file)

if __name__ == "__main__":
    output_file = main()
    print(output_file)
