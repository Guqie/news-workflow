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
        """运行 Google 新闻爬虫（扩充版检索策略）"""
        print("\n" + "="*60)
        print("1. 运行 Google 新闻爬虫")
        print("="*60)
        
        if self.sector == 'healthcare':
            keywords = [
                # 核心产业词（6个）
                "医药产业 发展",
                "生物医药 创新",
                "医疗健康 政策",
                "医保 改革",
                "中医药 产业",
                "医疗器械 创新",
                # 政策改革词（5个）
                "药监 改革",
                "健康产业 建设",
                "医疗保障 体系",
                "卫生健康 事业",
                "医改 政策",
                # 创新技术词（5个）
                "医养结合",
                "互联网医疗",
                "智慧医疗",
                "医疗AI",
                "数字健康",
                # 地域产业词（4个）
                "医药产业 北京",
                "生物医药 上海",
                "医疗健康 江苏",
                "医药产业 广东"
            ]
        else:  # education
            keywords = [
                # 核心人才词（6个）
                "人才政策 发展",
                "教育改革 创新",
                "人才培养 产业",
                "职业教育 发展",
                "高校 人才",
                "技能人才 培养",
                # 引进支持词（5个）
                "科技人才 引进",
                "青年人才 政策",
                "人才引进 支持",
                "高层次人才",
                "人才战略",
                # 教育创新词（5个）
                "人工智能 教育",
                "数字人才 培养",
                "产教融合",
                "校企合作",
                "双一流 建设",
                # 地域人才词（4个）
                "人才政策 北京",
                "人才引进 上海",
                "人才培养 江苏",
                "人才政策 广东"
            ]
        
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
        """运行通用新闻爬虫（替代滚动新闻爬虫）"""
        print("\n" + "="*60)
        print("3. 运行通用新闻爬虫")
        print("="*60)
        
        # 医疗健康板块的信源
        if self.sector == 'healthcare':
            sources = [
                {'name': '中国经济网', 'url': 'http://www.ce.cn/cysc/newmain/yc/jsxw/'},
                {'name': '人民网财经', 'url': 'https://finance.people.com.cn/GB/70846/index.html'},
                {'name': '中国财经医药', 'url': 'https://finance.china.com.cn/industry/medicine/live.shtml'},
                {'name': '中国科技网', 'url': 'https://www.stdaily.com/web/gdxw/node_324_2.html'}
            ]
        else:  # education
            sources = [
                {'name': '中国经济网', 'url': 'http://www.ce.cn/cysc/newmain/yc/jsxw/'},
                {'name': '中国西藏网', 'url': 'http://www.tibet.cn/cn/Instant/'},
                {'name': '中国科技网', 'url': 'https://www.stdaily.com/web/gdxw/node_324_2.html'}
            ]
        
        # 使用通用爬虫爬取每个信源
        for source in sources:
            print(f"\n📰 爬取: {source['name']}")
            cmd = [
                'python3', 'universal_crawler.py',
                '--sector', self.sector,
                '--url', source['url'],
                '--pages', '5'
            ]
            
            try:
                subprocess.run(cmd, cwd=self.script_dir, check=True)
            except Exception as e:
                print(f"  ⚠️  {source['name']} 爬取失败: {e}")
        
        print("✅ 通用新闻爬虫完成")
    
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
            f'{self.sector}_universal_{date_str}.json',  # 通用爬虫数据
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




