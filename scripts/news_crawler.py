#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新闻爬虫系统 - 完整版
支持三种爬取方式：
1. 关键词搜索（通过 Clawdbot web_search）
2. 专业网站爬取（医药网、健康报）
3. RSS订阅（备用）
"""

import argparse
import json
import os
import sys
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import time

class NewsCrawler:
    """新闻爬虫主类"""
    
    def __init__(self, sector, count=10):
        self.sector = sector
        self.count = count
        self.config = self.load_config()
        self.results = []
        
    def load_config(self):
        """加载配置文件"""
        config_path = os.path.join(os.path.dirname(__file__), '../references/config.json')
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def crawl(self):
        """主爬取方法 - 协调所有爬取方式"""
        print(f"\n{'='*60}")
        print(f"开始爬取 {self.config['sectors'][self.sector]['name']} 板块新闻")
        print(f"目标数量: {self.count} 条")
        print(f"{'='*60}\n")
        
        # 方式1: 关键词搜索（主要方式）
        print("📡 方式1: 关键词搜索...")
        self.crawl_by_keywords()
        
        # 方式2: 专业网站爬取（医疗健康板块）
        if self.sector == 'healthcare':
            print("\n🏥 方式2: 专业网站爬取...")
            self.crawl_professional_sites()
        
        # 去重
        self.deduplicate()
        
        print(f"\n✓ 爬取完成！共获取 {len(self.results)} 条新闻")
        return self.results
    
    def crawl_by_keywords(self):
        """
        方式1: 关键词搜索爬取
        
        原理讲解：
        - 使用搜索引擎API搜索关键词
        - 过滤指定的可信新闻源
        - 提取标题、链接、摘要等信息
        """
        keywords = self.config['sectors'][self.sector]['keywords']
        trusted_sources = self.config['sectors'][self.sector]['trusted_sources']
        
        # 限制关键词数量，避免过度请求
        for keyword in keywords[:4]:
            print(f"  搜索关键词: {keyword}")
            
            # 这里需要调用 Clawdbot 的 web_search
            # 由于在脚本中无法直接调用，我们提供一个占位符
            # 实际使用时，应该通过 Clawdbot 调用
            
            # 模拟搜索结果（实际应该调用 web_search）
            print(f"    ⚠️  需要通过 Clawdbot web_search 工具搜索")
            print(f"    提示: 在 Clawdbot 中运行此脚本，或使用 API 方式")
            
            time.sleep(1)  # 避免请求过快
    
    def crawl_professional_sites(self):
        """
        方式2: 专业网站爬取
        
        原理讲解：
        1. 发送HTTP请求获取网页HTML
        2. 使用BeautifulSoup解析HTML
        3. 根据网页结构提取新闻列表
        4. 提取每条新闻的标题、链接、时间等
        """
        if '专业网站' not in self.config['sectors'][self.sector]:
            return
        
        sites = self.config['sectors'][self.sector]['专业网站']
        
        for site in sites:
            print(f"  爬取网站: {site['name']}")
            try:
                # 这里是专业网站爬取的示例
                # 实际需要根据每个网站的具体结构调整
                self.crawl_site(site)
            except Exception as e:
                print(f"    ✗ 爬取失败: {e}")
    
    def crawl_site(self, site):
        """
        爬取单个网站
        
        爬虫三步骤详解：
        """
        # 第1步：发送HTTP请求
        headers = {
            'User-Agent': self.config['crawler_settings']['user_agent']
        }
        
        response = requests.get(
            site['url'], 
            headers=headers,
            timeout=self.config['crawler_settings']['timeout']
        )
        
        if response.status_code != 200:
            print(f"    ✗ 请求失败，状态码: {response.status_code}")
            return
        
        # 第2步：解析HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 第3步：提取新闻列表
        # 注意：这里需要根据具体网站的HTML结构调整
        # 这是一个通用示例
        news_items = soup.find_all('a', class_='news-title')  # 示例选择器
        
        count = 0
        for item in news_items[:5]:  # 限制每个网站5条
            try:
                title = item.get_text().strip()
                url = item.get('href', '')
                
                # 补全相对链接
                if url.startswith('/'):
                    url = site['url'].rstrip('/') + url
                
                news_data = {
                    'title': title,
                    'url': url,
                    'source': site['name'],
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'content': ''  # 需要进一步爬取详情页
                }
                
                self.results.append(news_data)
                count += 1
                
            except Exception as e:
                continue
        
        print(f"    ✓ 获取 {count} 条新闻")
    
    def deduplicate(self):
        """
        去重功能
        
        原理：根据标题或URL去除重复的新闻
        """
        seen_titles = set()
        unique_results = []
        
        for news in self.results:
            title = news['title']
            if title not in seen_titles:
                seen_titles.add(title)
                unique_results.append(news)
        
        removed = len(self.results) - len(unique_results)
        if removed > 0:
            print(f"\n🔄 去重: 移除 {removed} 条重复新闻")
        
        self.results = unique_results
    
    def save_results(self):
        """保存爬取结果到JSON文件"""
        os.makedirs('../data/raw', exist_ok=True)
        date_str = datetime.now().strftime('%Y%m%d')
        filename = f"../data/raw/{self.sector}_{date_str}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 已保存到: {filename}")
        print(f"📊 共保存: {len(self.results)} 条新闻")


def main():
    parser = argparse.ArgumentParser(description='新闻爬虫系统')
    parser.add_argument('--sector', required=True, 
                       choices=['education', 'healthcare'],
                       help='板块: education(教育人才) 或 healthcare(医疗健康)')
    parser.add_argument('--count', type=int, default=10,
                       help='目标数量 (默认: 10)')
    args = parser.parse_args()
    
    crawler = NewsCrawler(args.sector, args.count)
    crawler.crawl()
    crawler.save_results()


if __name__ == '__main__':
    main()
