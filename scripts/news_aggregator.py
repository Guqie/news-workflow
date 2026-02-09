#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一新闻聚合器 - 整合所有新闻源
"""

import json
import os
import subprocess
from datetime import datetime
from collections import defaultdict

class NewsAggregator:
    """统一新闻聚合器"""
    
    def __init__(self, sector, hours=24):
        self.sector = sector
        self.hours = hours
        self.all_news = []
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(self.script_dir, '../data/raw')
        
        # 加载配置
        config_path = os.path.join(self.script_dir, '../references/config.json')
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
    
    def run_google_news_crawler(self):
        """运行 Google 新闻爬虫"""
        print("\n" + "="*60)
        print("1. 运行 Google 新闻爬虫")
        print("="*60)
        
        if self.sector == 'healthcare':
            keywords = ["医药产业", "生物医药", "医疗健康", "医保改革"]
        else:
            keywords = ["人才政策", "教育改革", "人才培养", "职业教育"]
        
        cmd = [
            'python3', 'google_news_crawler.py',
            '--sector', self.sector,
            '--hours', str(self.hours),
            '--keywords'
        ] + keywords
        
        try:
            subprocess.run(cmd, cwd=self.script_dir, check=True)
            print("✅ Google 新闻爬虫完成")
        except Exception as e:
            print(f"❌ Google 新闻爬虫失败: {e}")
    
    def run_rss_crawler(self):
        """运行 RSS 新闻爬虫"""
        print("\n" + "="*60)
        print("2. 运行 RSS 新闻爬虫")
        print("="*60)
        
        cmd = ['python3', 'rss_news_crawler.py', '--sector', self.sector]
        
        try:
            subprocess.run(cmd, cwd=self.script_dir, check=True)
            print("✅ RSS 新闻爬虫完成")
        except Exception as e:
            print(f"❌ RSS 新闻爬虫失败: {e}")
    
    def run_rolling_news_crawler(self):
        """运行滚动新闻爬虫"""
        print("\n" + "="*60)
        print("3. 运行滚动新闻爬虫")
        print("="*60)
        
        # 中国经济网即时新闻
        cmd = [
            'python3', 'rolling_news_crawler.py',
            '--sector', self.sector,
            '--url', 'http://www.ce.cn/cysc/newmain/yc/jsxw/',
            '--pages', '3'
        ]
        
        try:
            subprocess.run(cmd, cwd=self.script_dir, check=True)
            print("✅ 滚动新闻爬虫完成")
        except Exception as e:
            print(f"❌ 滚动新闻爬虫失败: {e}")
    
    def run_newspaper_crawler(self):
        """运行 Newspaper4k 爬虫"""
        print("\n" + "="*60)
        print("4. 运行 Newspaper4k 新闻提取器")
        print("="*60)
        
        cmd = [
            'python3', 'newspaper_crawler.py',
            '--sector', self.sector,
            '--hours', str(self.hours)
        ]
        
        try:
            subprocess.run(cmd, cwd=self.script_dir, check=True)
            print("✅ Newspaper4k 爬虫完成")
        except Exception as e:
            print(f"❌ Newspaper4k 爬虫失败: {e}")
    
    def load_all_news(self):
        """加载所有爬取的新闻"""
        print("\n" + "="*60)
        print("5. 整合所有新闻数据")
        print("="*60)
        
        date_str = datetime.now().strftime('%Y%m%d')
        
        # 定义所有可能的数据文件
        file_patterns = [
            f'{self.sector}_google_{date_str}.json',
            f'{self.sector}_rss_{date_str}.json',
            f'{self.sector}_rolling_{date_str}.json',
            f'{self.sector}_newspaper_{date_str}.json'
        ]
        
        for pattern in file_patterns:
            file_path = os.path.join(self.data_dir, pattern)
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        news_list = json.load(f)
                        self.all_news.extend(news_list)
                        print(f"  ✓ 加载 {pattern}: {len(news_list)} 条")
                except Exception as e:
                    print(f"  ✗ 加载 {pattern} 失败: {e}")
        
        print(f"\n📊 总计加载: {len(self.all_news)} 条新闻")
    
    def deduplicate_and_sort(self):
        """去重和排序"""
        print("\n" + "="*60)
        print("5. 去重和排序")
        print("="*60)
        
        # 去重
        seen_titles = set()
        unique_news = []
        
        for news in self.all_news:
            title = news.get('title', '')
            if title and title not in seen_titles:
                seen_titles.add(title)
                unique_news.append(news)
        
        removed = len(self.all_news) - len(unique_news)
        print(f"  🔄 去重: 移除 {removed} 条重复新闻")
        
        self.all_news = unique_news
        print(f"  📊 去重后: {len(self.all_news)} 条新闻")
    
    def save_aggregated_results(self):
        """保存聚合结果"""
        print("\n" + "="*60)
        print("6. 保存聚合结果")
        print("="*60)
        
        if not self.all_news:
            print("⚠️  没有新闻数据")
            return
        
        date_str = datetime.now().strftime('%Y%m%d')
        output_file = os.path.join(self.data_dir, f'{self.sector}_aggregated_{date_str}.json')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.all_news, f, ensure_ascii=False, indent=2)
        
        print(f"  💾 已保存到: {output_file}")
        print(f"  📊 共保存: {len(self.all_news)} 条新闻")
        
        # 打印前10条标题
        print(f"\n📰 前10条新闻标题：")
        for i, news in enumerate(self.all_news[:10], 1):
            print(f"{i}. {news.get('title', '无标题')}")
    
    def run(self):
        """运行完整流程"""
        print("\n" + "🚀"*30)
        print(f"开始新闻聚合 - {self.config['sectors'][self.sector]['name']}")
        print(f"时间范围: 最近 {self.hours} 小时")
        print("🚀"*30)
        
        # 1. 运行 Google 新闻爬虫
        self.run_google_news_crawler()
        
        # 2. 运行 RSS 新闻爬虫 (已禁用 - 时效性差)
        # self.run_rss_crawler()
        
        # 3. 运行滚动新闻爬虫
        self.run_rolling_news_crawler()
        
        # 4. 运行 Newspaper4k 爬虫
        self.run_newspaper_crawler()
        
        # 5. 加载所有新闻
        self.load_all_news()
        
        # 6. 去重和排序
        self.deduplicate_and_sort()
        
        # 7. 保存聚合结果
        self.save_aggregated_results()
        
        print("\n" + "✅"*30)
        print("新闻聚合完成！")
        print("✅"*30)

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='统一新闻聚合器')
    parser.add_argument('--sector', required=True, choices=['healthcare', 'education'], 
                        help='板块: healthcare 或 education')
    parser.add_argument('--hours', type=int, default=24, help='时间范围（小时）')
    
    args = parser.parse_args()
    
    aggregator = NewsAggregator(args.sector, args.hours)
    aggregator.run()




