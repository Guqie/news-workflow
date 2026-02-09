#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
格式化新闻为markdown格式
按照用户要求的格式：
- 标题：
- 来源：
- 所属类别：
- 关键词：
- 发布时间：
- 链接：
- 摘要：
"""

import json
import os
from datetime import datetime
from pathlib import Path

def extract_keywords(title, summary=""):
    """简单的关键词提取（可以后续用AI优化）"""
    # 这里先返回空，后续可以集成AI提取
    return "待提取"

def format_news_item(item, sector_name):
    """格式化单条新闻"""
    title = item.get('title', '无标题')
    source = item.get('source', '未知来源')
    url = item.get('url', '#')
    published = item.get('published', '未知时间')
    summary = item.get('summary', item.get('description', ''))
    
    # 格式化输出
    output = f"""
## {title}

**标题：** {title}

**来源：** {source}

**所属类别：** {sector_name}

**关键词：** {extract_keywords(title, summary)}

**发布时间：** {published}

**链接：** {url}

**摘要：**
{summary if summary else '暂无摘要'}

---

"""
    return output

def generate_markdown_report(healthcare_file, education_file, output_file):
    """生成markdown格式报告"""
    report = []
    
    # 添加报告头部
    report.append(f"# 每日新闻资讯汇总\n")
    report.append(f"**生成时间：** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    report.append(f"**日期：** {datetime.now().strftime('%Y年%m月%d日')}\n")
    report.append("\n---\n")
    
    # 医疗健康板块
    if os.path.exists(healthcare_file):
        report.append("\n# 🏥 医疗健康板块\n")
        
        with open(healthcare_file, 'r', encoding='utf-8') as f:
            healthcare_data = json.load(f)
        
        report.append(f"\n**共收集 {len(healthcare_data)} 条新闻**\n")
        
        for item in healthcare_data:
            report.append(format_news_item(item, "医疗健康"))
    
    # 教育人才板块
    if os.path.exists(education_file):
        report.append("\n# 🎓 教育人才板块\n")
        
        with open(education_file, 'r', encoding='utf-8') as f:
            education_data = json.load(f)
        
        report.append(f"\n**共收集 {len(education_data)} 条新闻**\n")
        
        for item in education_data:
            report.append(format_news_item(item, "教育人才"))
    
    # 保存报告
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("".join(report))
    
    return output_file

def main():
    # 数据文件路径
    script_dir = Path(__file__).parent
    data_dir = script_dir.parent / "data" / "raw"
    date_str = datetime.now().strftime("%Y%m%d")
    
    healthcare_file = data_dir / f"healthcare_aggregated_{date_str}.json"
    education_file = data_dir / f"education_aggregated_{date_str}.json"
    
    # 输出文件
    output_file = data_dir / f"daily_news_{date_str}.md"
    
    # 生成报告
    result = generate_markdown_report(healthcare_file, education_file, output_file)
    
    print(f"✅ Markdown报告已生成：{result}")
    print(f"📊 文件大小：{Path(result).stat().st_size / 1024:.2f} KB")
    
    return str(result)

if __name__ == "__main__":
    output_file = main()
    print(output_file)
