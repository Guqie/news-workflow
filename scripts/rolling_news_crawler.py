#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
滚动新闻爬虫 - 支持关键词过滤和翻页
"""

import json
import os
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import time
import re

class RollingNewsCrawler:
    """滚动新闻爬虫 - 关键词过滤版"""
    
    def __init__(self, sector):
        self.sector = sector
        self.config = self.load_config()
        self.results = []
        self.session = requests.Session()
        
        # 设置请求头
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        })
        
        # 获取关键词
        self.keywords = self.config['sectors'][sector]['keywords']
    
    def load_config(self):
        """加载配置文件"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(script_dir, '../references/config.json')
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def match_keywords(self, title):
        """检查标题是否包含关键词"""
        for keyword in self.keywords:
            if keyword in title:
                return True
        return False
    
    def crawl_rolling_news(self, url, max_pages=3):
        """
        爬取滚动新闻
        
        参数:
            url: 新闻列表页URL
            max_pages: 最大翻页数
        """
        print(f"\n🔍 爬取滚动新闻: {url}")
        
        for page in range(1, max_pages + 1):
            print(f"  📄 第 {page} 页...")
            
            # 构造翻页URL
            page_url = self.build_page_url(url, page)
            
            try:
                response = self.session.get(page_url, timeout=10)
                
                # 根据网站设置编码
                if 'people.com.cn' in page_url:
                    response.encoding = 'gb2312'
                else:
                    response.encoding = 'utf-8'
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 查找新闻列表
                news_items = self.extract_news_list(soup, url)
                
                # 过滤关键词
                matched_count = 0
                for item in news_items:
                    if self.match_keywords(item['title']):
                        self.results.append(item)
                        matched_count += 1
                
                print(f"     ✓ 找到 {len(news_items)} 条新闻，匹配 {matched_count} 条")
                
                time.sleep(1)  # 礼貌延迟
                
            except Exception as e:
                print(f"     ✗ 爬取失败: {e}")
                break
        
        # 去重
        self.deduplicate()
    
    def build_page_url(self, base_url, page):
        """构造翻页URL"""
        # 不同网站的翻页规则不同
        if 'people.com.cn' in base_url:
            # 人民网: index.html -> index2.html, index3.html
            if page == 1:
                return base_url
            else:
                return base_url.replace('index.html', f'index{page}.html')
        elif 'sina.com.cn' in base_url:
            # 新浪: 使用page参数
            return base_url.replace('page=1', f'page={page}')
        else:
            # 默认：尝试添加page参数
            separator = '&' if '?' in base_url else '?'
            return f"{base_url}{separator}page={page}"
    
    def extract_news_list(self, soup, base_url):
        """从HTML中提取新闻列表"""
        news_items = []
        
        # 针对不同网站使用不同的策略
        if 'people.com.cn' in base_url:
            # 人民网：ul.list_16 li a
            news_items = self._extract_people_news(soup, base_url)
        elif 'ce.cn' in base_url:
            # 中国经济网：查找包含日期的链接
            news_items = self._extract_ce_news(soup, base_url)
        elif 'stdaily.com' in base_url:
            # 中国科技网
            news_items = self._extract_stdaily_news(soup, base_url)
        elif 'tibet.cn' in base_url:
            # 中国西藏网
            news_items = self._extract_tibet_news(soup, base_url)
        else:
            # 通用方法
            news_items = self._extract_generic_news(soup, base_url)
        
        return news_items
    
    def _extract_people_news(self, soup, base_url):
        """提取人民网新闻"""
        news_items = []
        uls = soup.find_all('ul', class_='list_16')
        
        for ul in uls:
            links = ul.find_all('a', href=True)
            for link in links:
                title = link.get_text().strip()
                href = link.get('href', '')
                
                if not title or len(title) < 10:
                    continue
                
                # 补全URL
                if href.startswith('/'):
                    from urllib.parse import urlparse
                    parsed = urlparse(base_url)
                    href = f"{parsed.scheme}://{parsed.netloc}{href}"
                
                news_items.append({
                    'title': title,
                    'url': href,
                    'source': '人民网滚动',
                    'date': datetime.now().strftime('%Y-%m-%d')
                })
        
        return news_items
    
    def _extract_ce_news(self, soup, base_url):
        """提取中国经济网新闻"""
        news_items = []
        all_links = soup.find_all('a', href=True)
        
        for link in all_links:
            title = link.get_text().strip()
            href = link.get('href', '')
            
            # 过滤：标题长度合适，且链接包含日期
            if title and 15 < len(title) < 100 and '/202' in href:
                # 补全URL
                if href.startswith('./'):
                    href = base_url + href[2:]
                elif href.startswith('/'):
                    href = 'http://www.ce.cn' + href
                
                news_items.append({
                    'title': title,
                    'url': href,
                    'source': '中国经济网',
                    'date': datetime.now().strftime('%Y-%m-%d')
                })
        
        return news_items
    
    def _extract_stdaily_news(self, soup, base_url):
        """提取中国科技网新闻"""
        news_items = []
        all_links = soup.find_all('a', href=True)
        
        for link in all_links:
            title = link.get_text().strip()
            href = link.get('href', '')
            
            # 过滤：标题长度合适，链接包含日期
            if title and 15 < len(title) < 100 and '/202' in href:
                # 补全URL
                if not href.startswith('http'):
                    href = 'https://www.stdaily.com' + href if href.startswith('/') else href
                
                news_items.append({
                    'title': title,
                    'url': href,
                    'source': '中国科技网',
                    'date': datetime.now().strftime('%Y-%m-%d')
                })
        
        return news_items
    
    def _extract_tibet_news(self, soup, base_url):
        """提取中国西藏网新闻"""
        news_items = []
        all_links = soup.find_all('a', href=True)
        
        for link in all_links:
            title = link.get_text().strip()
            href = link.get('href', '')
            
            # 过滤：标题长度合适
            if title and 15 < len(title) < 100:
                # 补全URL
                if href.startswith('./'):
                    href = base_url + href[2:]
                elif href.startswith('/'):
                    href = 'http://www.tibet.cn' + href
                
                news_items.append({
                    'title': title,
                    'url': href,
                    'source': '中国西藏网',
                    'date': datetime.now().strftime('%Y-%m-%d')
                })
        
        return news_items
    
    def _extract_generic_news(self, soup, base_url):
        """通用新闻提取方法"""
        news_items = []
        
        # 尝试多种选择器
        selectors = [
            'ul.news_list li a',
            'div.news-list li a',
            'ul.list li a',
            'div.list-item a',
        ]
        
        for selector in selectors:
            links = soup.select(selector)
            if links and len(links) > 5:
                for link in links[:50]:
                    title = link.get_text().strip()
                    href = link.get('href', '')
                    
                    if not title or len(title) < 10:
                        continue
                    
                    # 补全URL
                    if href.startswith('/'):
                        from urllib.parse import urlparse
                        parsed = urlparse(base_url)
                        href = f"{parsed.scheme}://{parsed.netloc}{href}"
                    elif not href.startswith('http'):
                        continue
                    
                    news_items.append({
                        'title': title,
                        'url': href,
                        'source': '滚动新闻',
                        'date': datetime.now().strftime('%Y-%m-%d')
                    })
                break
        
        return news_items
    
    def deduplicate(self):
        """去重功能"""
        seen_titles = set()
        seen_urls = set()
        unique_results = []
        
        for news in self.results:
            title = news['title']
            url = news['url']
            
            # 根据标题和URL去重
            if title not in seen_titles and url not in seen_urls:
                seen_titles.add(title)
                seen_urls.add(url)
                unique_results.append(news)
        
        removed = len(self.results) - len(unique_results)
        if removed > 0:
            print(f"\n🔄 去重: 移除 {removed} 条重复新闻")
        
        self.results = unique_results
    
    def save_results(self):
        """保存结果（追加模式）"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(script_dir, '../data/raw')
        os.makedirs(data_dir, exist_ok=True)
        
        date_str = datetime.now().strftime('%Y%m%d')
        filename = os.path.join(data_dir, f"{self.sector}_rolling_{date_str}.json")
        
        # 如果文件已存在，先加载现有数据
        existing_data = []
        if os.path.exists(filename):
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
            except:
                existing_data = []
        
        # 合并数据
        all_data = existing_data + self.results
        
        # 去重
        seen_urls = set()
        unique_data = []
        for item in all_data:
            url = item.get('url', '')
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_data.append(item)
        
        # 保存
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(unique_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 已保存到: {filename}")
        print(f"📊 共保存: {len(unique_data)} 条新闻（本次新增: {len(self.results)} 条）")


def main():
    import argparse
    parser = argparse.ArgumentParser(description='滚动新闻爬虫')
    parser.add_argument('--sector', required=True, 
                       choices=['education', 'healthcare'],
                       help='板块')
    parser.add_argument('--url', help='滚动新闻URL（单个爬取）')
    parser.add_argument('--all', action='store_true', help='爬取配置文件中的所有新闻源')
    parser.add_argument('--pages', type=int, default=10, help='翻页数')
    args = parser.parse_args()
    
    crawler = RollingNewsCrawler(args.sector)
    
    if args.all:
        # 批量爬取配置文件中的所有新闻源
        print(f"\n{'='*60}")
        print(f"批量爬取 {crawler.config['sectors'][args.sector]['name']} 板块的所有新闻源")
        print(f"{'='*60}")
        
        news_sources = crawler.config['sectors'][args.sector]['news_sources']
        for source in news_sources:
            print(f"\n📰 爬取: {source['name']}")
            crawler.crawl_rolling_news(source['url'], args.pages)
            time.sleep(2)  # 避免请求过快
    elif args.url:
        # 单个URL爬取
        crawler.crawl_rolling_news(args.url, args.pages)
    else:
        parser.error('请指定 --url 或 --all 参数')
    
    crawler.save_results()


if __name__ == '__main__':
    main()

