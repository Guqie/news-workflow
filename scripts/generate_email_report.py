#!/usr/bin/env python3
"""
生成详细版新闻报告并发送邮件
"""
import json
import sys
from datetime import datetime
from pathlib import Path

def load_json(file_path):
    """加载JSON文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ 加载文件失败 {file_path}: {e}")
        return []

def format_news_item(item, index):
    """格式化单条新闻（详细版）"""
    title = item.get('title', '无标题')
    source = item.get('source', '未知来源')
    url = item.get('url', '#')
    published = item.get('published', '未知时间')
    summary = item.get('summary', item.get('description', ''))
    
    # 格式化输出
    output = f"\n{'='*80}\n"
    output += f"【{index}】{title}\n"
    output += f"来源：{source}\n"
    output += f"时间：{published}\n"
    output += f"链接：{url}\n"
    
    if summary:
        output += f"\n摘要：\n{summary}\n"
    
    return output

def generate_report(healthcare_file, education_files):
    """生成详细版报告"""
    report = []
    
    # 添加报告头部
    report.append("="*80)
    report.append(f"每日新闻资讯汇总 - 详细版")
    report.append(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("="*80)
    
    # 医疗健康板块
    report.append("\n\n" + "🏥 " + "="*76)
    report.append("医疗健康板块")
    report.append("="*80)
    
    healthcare_data = load_json(healthcare_file)
    report.append(f"\n共收集 {len(healthcare_data)} 条新闻\n")
    
    for idx, item in enumerate(healthcare_data[:50], 1):  # 限制前50条
        report.append(format_news_item(item, idx))
    
    if len(healthcare_data) > 50:
        report.append(f"\n... 还有 {len(healthcare_data) - 50} 条新闻未显示 ...\n")
    
    # 教育人才板块
    report.append("\n\n" + "🎓 " + "="*76)
    report.append("教育人才板块")
    report.append("="*80)
    
    # 合并教育人才的所有数据
    education_data = []
    for file_path in education_files:
        data = load_json(file_path)
        education_data.extend(data)
    
    # 去重
    seen_urls = set()
    unique_education_data = []
    for item in education_data:
        url = item.get('url', '')
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique_education_data.append(item)
    
    report.append(f"\n共收集 {len(unique_education_data)} 条新闻（已去重）\n")
    
    for idx, item in enumerate(unique_education_data[:50], 1):  # 限制前50条
        report.append(format_news_item(item, idx))
    
    if len(unique_education_data) > 50:
        report.append(f"\n... 还有 {len(unique_education_data) - 50} 条新闻未显示 ...\n")
    
    # 报告尾部
    report.append("\n\n" + "="*80)
    report.append("报告结束")
    report.append("="*80)
    
    return "\n".join(report)

def main():
    # 数据文件路径
    data_dir = Path(__file__).parent.parent / "data" / "raw"
    date_str = datetime.now().strftime("%Y%m%d")
    
    healthcare_file = data_dir / f"healthcare_aggregated_{date_str}.json"
    education_files = [
        data_dir / f"education_google_{date_str}.json",
        data_dir / f"education_rss_{date_str}.json",
        data_dir / f"education_rolling_{date_str}.json"
    ]
    
    # 生成报告
    report = generate_report(healthcare_file, education_files)
    
    # 保存到文件
    output_file = data_dir / f"daily_report_{date_str}.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✅ 报告已生成：{output_file}")
    print(f"📊 文件大小：{output_file.stat().st_size / 1024:.2f} KB")
    
    return str(output_file)

if __name__ == "__main__":
    output_file = main()
    print(output_file)
