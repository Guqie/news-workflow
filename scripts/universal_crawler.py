#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用新闻爬虫 - 自动识别网页结构
只需提供URL，自动提取新闻列表
"""

import json
import os
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import time
import re
from urllib.parse import urljoin
import urllib3

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class UniversalNewsCrawler:
    """通用新闻爬虫 - 自动识别网页结构"""
    
    def __init__(self, sector):
        self.sector = sector
        self.results = []
        self.session = requests.Session()
        
        # 设置请求头
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        })
        
        # 加载关键词
        self.keywords = self.load_keywords()
    
    def load_keywords(self):
        """加载关键词"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(script_dir, '../references/config.json')
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return config['sectors'][self.sector]['keywords']
        except:
            # 默认关键词
            if self.sector == 'healthcare':
                return ['医疗', '健康', '医药', '医院', '医保']
            else:
                return ['教育', '人才', '高校', '培训', '就业']
    
    def auto_detect_news_list(self, soup, base_url):
        """自动识别新闻列表 - 增强版"""
        news_items = []
        seen_urls = set()
        
        # 策略1: 查找常见新闻列表容器
        patterns = [
            r'(list|news|item|article|content)',
            r'(roll|scroll|feed)',
            r'(main|body|center)'
        ]
        
        for pattern in patterns:
            containers = soup.find_all(['ul', 'ol', 'div', 'section'], 
                                      class_=re.compile(pattern, re.I))
            
            for container in containers:
                links = container.find_all('a', href=True)
                if len(links) >= 3:  # 降低阈值到3个
                    for link in links[:100]:
                        title = link.get_text(strip=True)
                        url = urljoin(base_url, link['href'])
                        
                        # 提取日期
                        published = self._extract_date(link.parent)
                        
                        # 过滤条件
                        if (title and 
                            len(title) >= 8 and len(title) <= 150 and
                            url not in seen_urls and
                            not self._is_invalid_link(url)):
                            
                            seen_urls.add(url)
                            news_items.append({
                                'title': title,
                                'url': url,
                                'source': base_url,
                                'published': published
                            })
            
            if len(news_items) >= 20:
                break
        
        # 策略2: 查找带时间标记的链接
        if len(news_items) < 10:
            time_patterns = [r'\d{4}-\d{2}-\d{2}', r'\d{2}:\d{2}', r'\d{2}/\d{2}']
            all_links = soup.find_all('a', href=True)
            
            for link in all_links[:200]:
                parent = link.parent
                if parent:
                    parent_text = parent.get_text()
                    has_time = any(re.search(p, parent_text) for p in time_patterns)
                    
                    if has_time:
                        title = link.get_text(strip=True)
                        url = urljoin(base_url, link['href'])
                        published = self._extract_date(parent)
                        
                        if (title and len(title) >= 8 and 
                            url not in seen_urls and
                            not self._is_invalid_link(url)):
                            
                            seen_urls.add(url)
                            news_items.append({
                                'title': title,
                                'url': url,
                                'source': base_url,
                                'published': published
                            })
        
        return news_items
    
    def _extract_date(self, element):
        """提取日期时间"""
        if not element:
            return None
        
        text = element.get_text()
        
        # 日期格式
        date_patterns = [
            r'\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}',  # 2026-02-09 14:30
            r'\d{4}/\d{2}/\d{2}\s+\d{2}:\d{2}',  # 2026/02/09 14:30
            r'\d{4}年\d{2}月\d{2}日',            # 2026年02月09日
            r'\d{2}-\d{2}\s+\d{2}:\d{2}',        # 02-09 14:30
            r'\d{2}/\d{2}\s+\d{2}:\d{2}',        # 02/09 14:30
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group()
        
        return None
    
    def _is_invalid_link(self, url):
        """判断是否为无效链接"""
        invalid_patterns = [
            r'javascript:', r'#', r'mailto:', 
            r'\.(jpg|png|gif|pdf|zip|rar)$',
            r'(login|register|about|contact)'
        ]
        return any(re.search(p, url, re.I) for p in invalid_patterns)
    
    def match_keywords(self, title):
        """关键词匹配 - 增强版"""
        # 基础匹配
        for keyword in self.keywords:
            if keyword in title:
                return True
        
        # 扩展匹配：同义词和相关词
        if self.sector == 'healthcare':
            extended_keywords = [
                '药企', '药厂', '制药', '新药', '仿制药',
                '医生', '护士', '患者', '病人',
                '诊所', '卫生', '疾控', 'CDC',
                '医学', '临床', '手术', '治疗'
            ]
        else:  # education
            extended_keywords = [
                '学生', '教师', '老师', '校长',
                '大学生', '研究生', '博士', '硕士',
                '招生', '考试', '升学', '毕业',
                '科研', '学术', '论文', '课题'
            ]
        
        for keyword in extended_keywords:
            if keyword in title:
                return True
        
        return False
    
    def crawl_url(self, url, max_pages=3):
        """爬取单个URL（支持翻页）"""
        print(f"\n🔍 爬取: {url}")
        
        for page in range(1, max_pages + 1):
            try:
                # 构造翻页URL
                page_url = self._build_page_url(url, page)
                
                print(f"  📄 第 {page} 页...")
                
                # 禁用SSL验证
                response = self.session.get(page_url, timeout=10, verify=False)
                response.encoding = response.apparent_encoding or 'utf-8'
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 自动识别新闻列表
                news_items = self.auto_detect_news_list(soup, url)
                
                if not news_items:
                    print(f"     ✗ 未找到新闻，停止翻页")
                    break
                
                # 关键词过滤
                matched = 0
                for item in news_items:
                    if self.match_keywords(item['title']):
                        item['crawled_at'] = datetime.now().isoformat()
                        self.results.append(item)
                        matched += 1
                
                print(f"     ✓ 找到 {len(news_items)} 条新闻，匹配 {matched} 条")
                
                time.sleep(1)  # 礼貌延迟
                
            except Exception as e:
                print(f"     ✗ 第 {page} 页爬取失败: {e}")
                break
    
    def _build_page_url(self, base_url, page):
        """构造翻页URL - 增强版"""
        if page == 1:
            return base_url
        
        # 常见翻页模式（按优先级排序）
        patterns = [
            # 模式1: index.html -> index_2.html
            (r'index\.html$', f'index_{page}.html'),
            # 模式2: index.html -> index_2.htm
            (r'index\.htm$', f'index_{page}.htm'),
            # 模式3: /path/ -> /path/2/
            (r'/$', f'{page}/'),
            # 模式4: /path/index.html -> /path/index_2.html
            (r'/index\.html$', f'/index_{page}.html'),
            # 模式5: .html -> _2.html
            (r'\.html$', f'_{page}.html'),
            # 模式6: .htm -> _2.htm
            (r'\.htm$', f'_{page}.htm'),
            # 模式7: /node_324_2.html -> /node_324_3.html
            (r'_(\d+)\.html$', f'_{page}.html'),
        ]
        
        for pattern, replacement in patterns:
            if re.search(pattern, base_url):
                return re.sub(pattern, replacement, base_url)
        
        # 默认：添加page参数
        separator = '&' if '?' in base_url else '?'
        return f"{base_url}{separator}page={page}"
    
    def save_results(self):
        """保存结果（追加模式 + 智能去重）"""
        if not self.results:
            print("\n⚠️  没有找到匹配的新闻")
            return
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(script_dir, '../data/raw')
        os.makedirs(data_dir, exist_ok=True)
        
        date_str = datetime.now().strftime('%Y%m%d')
        filename = os.path.join(data_dir, f"{self.sector}_universal_{date_str}.json")
        
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
        
        # 智能去重：URL + 标题相似度
        unique_data = []
        seen_urls = set()
        seen_titles = set()
        
        for item in all_data:
            url = item.get('url', '')
            title = item.get('title', '')
            
            # URL去重
            if url in seen_urls:
                continue
            
            # 标题相似度去重（简化版）
            title_key = self._normalize_title(title)
            if title_key in seen_titles:
                continue
            
            seen_urls.add(url)
            seen_titles.add(title_key)
            unique_data.append(item)
        
        # 保存
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(unique_data, f, ensure_ascii=False, indent=2)
        
        removed = len(all_data) - len(unique_data)
        print(f"\n💾 已保存到: {filename}")
        print(f"📊 共保存: {len(unique_data)} 条新闻（本次新增: {len(self.results)} 条，去重: {removed} 条）")
    
    def _normalize_title(self, title):
        """标题归一化（用于去重）"""
        # 移除空格、标点
        normalized = re.sub(r'[\s\-_—\|｜]', '', title)
        # 只保留前30个字符
        return normalized[:30]

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='通用新闻爬虫')
    parser.add_argument('--sector', required=True, choices=['healthcare', 'education'],
                        help='板块: healthcare 或 education')
    parser.add_argument('--url', required=True, help='新闻网站URL')
    parser.add_argument('--pages', type=int, default=3, help='翻页数（暂不支持）')
    
    args = parser.parse_args()
    
    crawler = UniversalNewsCrawler(args.sector)
    crawler.crawl_url(args.url, args.pages)
    crawler.save_results()

