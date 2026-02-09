#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新闻爬虫系统 - 增强版
支持多种新闻源的爬取
"""

import json
import os
import sys
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import time
import re

class EnhancedNewsCrawler:
    """增强版新闻爬虫"""
    
    def __init__(self, sector, count=10):
        self.sector = sector
        self.count = count
        self.config = self.load_config()
        self.results = []
        self.session = requests.Session()
        
        # 设置请求头
        self.session.headers.update({
            'User-Agent': self.config['crawler_settings']['user_agent'],
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
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
        print(f"🕷️  新闻爬虫 - {self.config['sectors'][self.sector]['name']}")
        print(f"📊 目标数量: {self.count} 条")
        print(f"{'='*60}\n")
        
        # 爬取配置的新闻源
        news_sources = self.config['sectors'][self.sector].get('news_sources', [])
        
        for source in news_sources:
            print(f"📍 {source['name']}")
            self.crawl_source(source)
            time.sleep(2)  # 礼貌延迟
        
        # 去重
        self.deduplicate()
        
        print(f"\n✅ 爬取完成！共获取 {len(self.results)} 条新闻")
        return self.results
    
    def crawl_source(self, source):
        """根据不同的网站类型选择爬取方法"""
        try:
            # 健康报行业快讯 - 特殊处理（JSON提取）
            if source['name'] == '健康报行业快讯':
                self.crawl_jkb_industry_news()
            # 医药网最新资讯
            elif source['name'] == '医药网最新资讯':
                self.crawl_pharmnet_news(source['url'])
            # 国家医疗保障局
            elif source['name'] == '国家医疗保障局':
                self.crawl_nhsa(source)
            # 国家卫生健康委员会
            elif source['name'] == '国家卫生健康委员会':
                self.crawl_nhc(source)
            # 其他通用网站
            else:
                self.crawl_generic_site(source)
                
        except Exception as e:
            print(f"  ✗ 爬取失败: {e}")
    
    def crawl_jkb_industry_news(self):
        """爬取健康报行业快讯（JSON提取方式）"""
        try:
            url = 'https://www.jkb.com.cn/news/industryNews'
            response = self.session.get(url, timeout=10)
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.text, 'html.parser')
            data_div = soup.find('div', id='ttde_data')
            
            if data_div:
                json_text = data_div.get_text().strip()
                news_list = json.loads(json_text)
                
                count = 0
                for news in news_list[:5]:  # 限制5条
                    news_data = {
                        'title': news['title'],
                        'url': f"https://www.jkb.com.cn/news/industryNews/{news['url']}",
                        'source': '健康报',
                        'date': datetime.now().strftime('%Y-%m-%d'),
                        'summary': news['description'][:200]
                    }
                    self.results.append(news_data)
                    count += 1
                
                print(f"  ✓ 获取 {count} 条新闻")
            else:
                print(f"  ✗ 未找到数据")
                
        except Exception as e:
            print(f"  ✗ 爬取失败: {e}")
    
    def crawl_pharmnet_news(self, url):
        """爬取医药网最新资讯"""
        try:
            response = self.session.get(url, timeout=10)
            response.encoding = 'gbk'  # 医药网使用gbk编码
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找新闻列表
            news_links = soup.find_all('a', href=re.compile(r'/news/\d+/\d+/\d+/\d+\.html'))
            
            count = 0
            for link in news_links[:5]:  # 限制5条
                title = link.get_text().strip()
                href = link.get('href', '')
                
                if not title or len(title) < 10:
                    continue
                
                if href.startswith('/'):
                    href = 'https://news.pharmnet.com.cn' + href
                
                news_data = {
                    'title': title,
                    'url': href,
                    'source': '医药网',
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'summary': ''
                }
                
                self.results.append(news_data)
                count += 1
            
            print(f"  ✓ 获取 {count} 条新闻")
            
        except Exception as e:
            print(f"  ✗ 爬取失败: {e}")
    
    def crawl_generic_site(self, source):
        """通用网站爬取方法"""
        try:
            response = self.session.get(source['url'], timeout=10)
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 通用的新闻链接查找
            news_links = soup.find_all('a', href=True)
            
            count = 0
            for link in news_links:
                title = link.get_text().strip()
                href = link.get('href', '')
                
                # 过滤条件
                if not title or len(title) < 10 or len(title) > 100:
                    continue
                
                # 补全URL
                if href.startswith('/'):
                    from urllib.parse import urlparse
                    parsed = urlparse(source['url'])
                    href = f"{parsed.scheme}://{parsed.netloc}{href}"
                elif not href.startswith('http'):
                    continue
                
                news_data = {
                    'title': title,
                    'url': href,
                    'source': source['name'],
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'summary': ''
                }
                
                self.results.append(news_data)
                count += 1
                
                if count >= 3:  # 每个通用网站限制3条
                    break
            
            print(f"  ✓ 获取 {count} 条新闻")
            
        except Exception as e:
            print(f"  ✗ 爬取失败: {e}")
    
    def crawl_nhsa(self, source):
        """爬取国家医疗保障局"""
        try:
            urls = source.get('urls', [])
            limit = source.get('limit', 3)
            total_count = 0
            
            for url in urls:
                response = self.session.get(url, timeout=10)
                response.encoding = source.get('encoding', 'utf-8')
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 查找新闻列表 - 使用正确的选择器
                news_list = soup.find('ul', class_='infoList')
                if not news_list:
                    continue
                
                news_links = news_list.find_all('a', href=True)
                
                count = 0
                for link in news_links:
                    if count >= limit:
                        break
                    
                    title = link.get_text().strip()
                    href = link.get('href', '')
                    
                    # 过滤：只要有实际标题的链接
                    if not title or len(title) < 10:
                        continue
                    
                    # 补全URL
                    if href.startswith('./'):
                        href = url.rsplit('/', 1)[0] + '/' + href[2:]
                    elif href.startswith('/'):
                        href = 'https://www.nhsa.gov.cn' + href
                    elif not href.startswith('http'):
                        href = 'https://www.nhsa.gov.cn' + href
                    
                    news_data = {
                        'title': title,
                        'url': href,
                        'source': '国家医保局',
                        'date': datetime.now().strftime('%Y-%m-%d'),
                        'summary': ''
                    }
                    
                    self.results.append(news_data)
                    count += 1
                    total_count += 1
            
            print(f"  ✓ 获取 {total_count} 条新闻")
            
        except Exception as e:
            print(f"  ✗ 爬取失败: {e}")
    
    def crawl_nhc(self, source):
        """爬取国家卫生健康委员会"""
        try:
            # 国家卫健委有反爬虫，需要特殊处理
            print(f"  ⚠️  国家卫健委有反爬虫机制，暂时跳过")
            print(f"  💡 建议：使用浏览器自动化或RSS订阅")
            
        except Exception as e:
            print(f"  ✗ 爬取失败: {e}")
    
    def deduplicate(self):
        """去重功能"""
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
        """保存结果"""
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
    parser = argparse.ArgumentParser(description='增强版新闻爬虫')
    parser.add_argument('--sector', required=True, 
                       choices=['education', 'healthcare'],
                       help='板块: education 或 healthcare')
    parser.add_argument('--count', type=int, default=10,
                       help='目标数量')
    args = parser.parse_args()
    
    crawler = EnhancedNewsCrawler(args.sector, args.count)
    crawler.crawl()
    crawler.save_results()


if __name__ == '__main__':
    main()
