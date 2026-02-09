#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MVP版本：使用RSS订阅
最简单、最稳定的方案
"""

import feedparser
from datetime import datetime, timedelta

def fetch_rss_news(rss_url, source_name, max_results=5):
    """
    从RSS源获取新闻
    """
    print(f"\n🔍 正在获取: {source_name}")
    print("-" * 60)
    
    try:
        feed = feedparser.parse(rss_url)
        
        if feed.bozo:
            print(f"❌ RSS解析失败")
            return []
        
        results = []
        now = datetime.now()
        one_day_ago = now - timedelta(days=1)
        
        for i, entry in enumerate(feed.entries[:max_results]):
            try:
                title = entry.title
                link = entry.link
                
                # 尝试获取发布时间
                pub_date = None
                if hasattr(entry, 'published_parsed'):
                    pub_date = datetime(*entry.published_parsed[:6])
                
                results.append({
                    'title': title,
                    'link': link,
                    'published': pub_date
                })
                
                print(f"{i+1}. {title}")
                if pub_date:
                    print(f"   📅 {pub_date.strftime('%Y-%m-%d %H:%M')}")
                print(f"   🔗 {link[:80]}...\n")
                
            except Exception as e:
                continue
        
        return results
        
    except Exception as e:
        print(f"❌ 获取失败: {e}")
        return []

def main():
    """
    主函数：测试RSS订阅
    """
    print("\n" + "="*60)
    print("📰 新闻爬虫 MVP - RSS版本")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # RSS源列表（使用可靠的RSS源）
    rss_sources = {
        "教育人才": [
            ("人民网教育", "http://edu.people.com.cn/rss/education.xml"),
        ],
        "医疗健康": [
            ("人民网健康", "http://health.people.com.cn/rss/health.xml"),
        ]
    }
    
    all_results = {}
    
    for sector, sources in rss_sources.items():
        print(f"\n📋 {sector}板块")
        print("="*60)
        all_results[sector] = []
        
        for source_name, rss_url in sources:
            results = fetch_rss_news(rss_url, source_name, max_results=5)
            all_results[sector].extend(results)
    
    # 统计
    print("\n" + "="*60)
    print("📊 统计结果")
    print("="*60)
    for sector, results in all_results.items():
        print(f"{sector}: {len(results)} 条新闻")
    print("\n✅ MVP测试完成！")

if __name__ == '__main__':
    main()
