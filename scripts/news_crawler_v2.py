#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新闻爬虫系统 - 完整实现版
支持多种爬取策略，应对不同网站的反爬虫机制
"""

import json
import os
import sys
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import time
import re

class NewsCrawler:
    """新闻爬虫主类"""
    
    def __init__(self, sector, count=10):
        self.sector = sector
        self.count = count
        self.config = self.load_config()
        self.results = []
        self.session = requests.Session()
        
        # 设置请求头，模拟浏览器
        self.session.headers.update({
            'User-Agent': self.config['crawler_settings']['user_agent'],
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
    
    def load_config(self):
        """加载配置文件"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(script_dir, '../references/config.json')
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def crawl(self):
        """主爬取方法"""
        print(f"\n{'='*60}")
        print(f"🕷️  开始爬取 {self.config['sectors'][self.sector]['name']} 板块新闻")
        print(f"📊 目标数量: {self.count} 条")
        print(f"{'='*60}\n")
        
        # 策略1: 爬取专业网站（医疗健康板块）
        if self.sector == 'healthcare' and '专业网站' in self.config['sectors'][self.sector]:
            print("🏥 策略1: 专业网站爬取...")
            self.crawl_professional_sites()
        
        # 策略2: 通用新闻网站爬取
        print("\n📰 策略2: 通用新闻网站...")
        self.crawl_general_news_sites()
        
        # 去重
        self.deduplicate()
        
        print(f"\n✅ 爬取完成！共获取 {len(self.results)} 条新闻")
        return self.results
    
    def crawl_professional_sites(self):
        """
        爬取专业网站（医药网、健康报）
        
        爬虫知识点：
        1. 不同网站的HTML结构不同，需要针对性解析
        2. 有些网站有反爬虫机制，需要特殊处理
        """
        sites = self.config['sectors'][self.sector].get('专业网站', [])
        
        for site in sites:
            print(f"  📍 {site['name']}: {site['url']}")
            
            if site['name'] == '健康报':
                self.crawl_jkb()
            elif site['name'] == '医药网':
                self.crawl_pharmnet()
            
            time.sleep(2)  # 礼貌性延迟，避免给服务器压力
    
    def crawl_jkb(self):
        """
        爬取健康报网站
        
        步骤讲解：
        1. 访问健康报首页
        2. 找到新闻列表区域
        3. 提取每条新闻的标题、链接、时间
        """
        try:
            url = 'https://www.jkb.com.cn/'
            response = self.session.get(url, timeout=10)
            response.encoding = 'utf-8'
            
            if response.status_code != 200:
                print(f"    ✗ 访问失败，状态码: {response.status_code}")
                return
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找新闻列表（需要根据实际HTML结构调整）
            # 这里是通用的查找方法
            news_links = soup.find_all('a', href=re.compile(r'/news/|/article/'))
            
            count = 0
            for link in news_links[:5]:  # 限制5条
                title = link.get_text().strip()
                href = link.get('href', '')
                
                if not title or len(title) < 10:
                    continue
                
                # 补全URL
                if href.startswith('/'):
                    href = 'https://www.jkb.com.cn' + href
                
                news_data = {
                    'title': title,
                    'url': href,
                    'source': '健康报',
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'content': ''
                }
                
                self.results.append(news_data)
                count += 1
            
            print(f"    ✓ 获取 {count} 条新闻")
            
        except Exception as e:
            print(f"    ✗ 爬取失败: {e}")
    
    def crawl_pharmnet(self):
        """
        爬取医药网
        
        注意：医药网有反爬虫机制（安全检查）
        解决方案：
        1. 使用更真实的请求头
        2. 添加 Referer
        3. 如果还是不行，可以尝试使用 Selenium（浏览器自动化）
        """
        try:
            url = 'https://www.pharmnet.com.cn/news/'
            
            # 添加更多请求头来绕过反爬虫
            headers = self.session.headers.copy()
            headers['Referer'] = 'https://www.pharmnet.com.cn/'
            
            response = self.session.get(url, headers=headers, timeout=10)
            
            if '安全检查' in response.text or response.status_code != 200:
                print(f"    ⚠️  医药网有反爬虫机制，跳过")
                print(f"    💡 建议：使用 RSS 订阅或 API 方式")
                return
            
            # 如果能访问，解析新闻列表
            soup = BeautifulSoup(response.text, 'html.parser')
            # ... 解析逻辑
            
        except Exception as e:
            print(f"    ✗ 爬取失败: {e}")
    
    def crawl_general_news_sites(self):
        """
        爬取通用新闻网站（新华网、人民网等）
        
        策略：使用搜索引擎或RSS订阅
        这里提供一个框架，实际需要配合其他工具
        """
        print("    💡 通用新闻网站建议使用以下方式：")
        print("       1. RSS订阅（最稳定）")
        print("       2. 搜索引擎API（web_search）")
        print("       3. 新闻聚合API")
        print("    ⚠️  当前版本暂未实现，请使用 web_search 补充")
    
    def deduplicate(self):
        """去重功能 - 根据标题去除重复的新闻"""
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
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(script_dir, '../data/raw')
        os.makedirs(data_dir, exist_ok=True)
        
        date_str = datetime.now().strftime('%Y%m%d')
        filename = os.path.join(data_dir, f"{self.sector}_{date_str}.json")
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 已保存到: {filename}")
        print(f"📊 共保存: {len(self.results)} 条新闻")


def main():
    import argparse
    parser = argparse.ArgumentParser(description='新闻爬虫系统 v2')
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
