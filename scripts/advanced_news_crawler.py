#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高级新闻爬虫 - 支持JavaScript渲染的网站
使用Selenium + Chrome Headless
"""

import json
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class AdvancedNewsCrawler:
    """高级新闻爬虫 - 支持JS渲染"""
    
    def __init__(self, sector):
        self.sector = sector
        self.results = []
        self.config = self.load_config()
        self.keywords = self.config['sectors'][sector]['keywords']
        
        # 初始化Chrome浏览器（无头模式）
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.set_page_load_timeout(30)
    
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
    
    def crawl_mohrss(self):
        """爬取人社部地方动态"""
        url = "https://www.mohrss.gov.cn/SYrlzyhshbzb/dongtaixinwen/dfdt/"
        print(f"\n🔍 爬取: 人社部地方动态")
        
        try:
            self.driver.get(url)
            time.sleep(3)  # 等待页面加载
            
            # 查找新闻列表
            news_items = self.driver.find_elements(By.CSS_SELECTOR, "ul.list_16 li a")
            
            for item in news_items[:30]:  # 限制数量
                try:
                    title = item.text.strip()
                    href = item.get_attribute('href')
                    
                    if title and len(title) > 10 and self.match_keywords(title):
                        self.results.append({
                            'title': title,
                            'url': href,
                            'source': '人社部',
                            'date': datetime.now().strftime('%Y-%m-%d')
                        })
                except:
                    continue
            
            print(f"  ✓ 找到 {len([r for r in self.results if r['source']=='人社部'])} 条匹配新闻")
        except Exception as e:
            print(f"  ✗ 爬取失败: {e}")
    
    def crawl_cs_com_cn(self):
        """爬取中国证券报财经要闻"""
        url = "https://www.cs.com.cn/xwzx/hg/"
        print(f"\n🔍 爬取: 中国证券报财经要闻")
        
        try:
            self.driver.get(url)
            time.sleep(3)
            
            # 查找新闻列表
            news_items = self.driver.find_elements(By.CSS_SELECTOR, "div.news-list li a, ul.news-list li a")
            
            for item in news_items[:30]:
                try:
                    title = item.text.strip()
                    href = item.get_attribute('href')
                    
                    if title and len(title) > 10 and self.match_keywords(title):
                        if not href.startswith('http'):
                            href = 'https://www.cs.com.cn' + href
                        
                        self.results.append({
                            'title': title,
                            'url': href,
                            'source': '中国证券报',
                            'date': datetime.now().strftime('%Y-%m-%d')
                        })
                except:
                    continue
            
            print(f"  ✓ 找到 {len([r for r in self.results if r['source']=='中国证券报'])} 条匹配新闻")
        except Exception as e:
            print(f"  ✗ 爬取失败: {e}")
    
    def crawl_cls_cn(self):
        """爬取财联社头条"""
        url = "https://www.cls.cn/depth?id=1000"
        print(f"\n🔍 爬取: 财联社头条")
        
        try:
            self.driver.get(url)
            time.sleep(3)
            
            # 查找新闻列表
            news_items = self.driver.find_elements(By.CSS_SELECTOR, "div.depth-item a.item-title")
            
            for item in news_items[:30]:
                try:
                    title = item.text.strip()
                    href = item.get_attribute('href')
                    
                    if title and len(title) > 10 and self.match_keywords(title):
                        if not href.startswith('http'):
                            href = 'https://www.cls.cn' + href
                        
                        self.results.append({
                            'title': title,
                            'url': href,
                            'source': '财联社',
                            'date': datetime.now().strftime('%Y-%m-%d')
                        })
                except:
                    continue
            
            print(f"  ✓ 找到 {len([r for r in self.results if r['source']=='财联社'])} 条匹配新闻")
        except Exception as e:
            print(f"  ✗ 爬取失败: {e}")
    
    def crawl_guandian_cn(self):
        """爬取观点网资讯"""
        url = "https://www.guandian.cn/news/"
        print(f"\n🔍 爬取: 观点网资讯")
        
        try:
            self.driver.get(url)
            time.sleep(3)
            
            news_items = self.driver.find_elements(By.CSS_SELECTOR, "div.news-item a, li.news-item a")
            
            for item in news_items[:30]:
                try:
                    title = item.text.strip()
                    href = item.get_attribute('href')
                    
                    if title and len(title) > 10 and self.match_keywords(title):
                        if not href.startswith('http'):
                            href = 'https://www.guandian.cn' + href
                        
                        self.results.append({
                            'title': title,
                            'url': href,
                            'source': '观点网',
                            'date': datetime.now().strftime('%Y-%m-%d')
                        })
                except:
                    continue
            
            print(f"  ✓ 找到 {len([r for r in self.results if r['source']=='观点网'])} 条匹配新闻")
        except Exception as e:
            print(f"  ✗ 爬取失败: {e}")
    
    def crawl_jjckb(self):
        """爬取经济参考报要闻"""
        url = "http://jjckb.xinhuanet.com/yw.htm"
        print(f"\n🔍 爬取: 经济参考报要闻")
        
        try:
            self.driver.get(url)
            time.sleep(3)
            
            news_items = self.driver.find_elements(By.CSS_SELECTOR, "ul.news-list li a, div.news-list a")
            
            for item in news_items[:30]:
                try:
                    title = item.text.strip()
                    href = item.get_attribute('href')
                    
                    if title and len(title) > 10 and self.match_keywords(title):
                        self.results.append({
                            'title': title,
                            'url': href,
                            'source': '经济参考报',
                            'date': datetime.now().strftime('%Y-%m-%d')
                        })
                except:
                    continue
            
            print(f"  ✓ 找到 {len([r for r in self.results if r['source']=='经济参考报'])} 条匹配新闻")
        except Exception as e:
            print(f"  ✗ 爬取失败: {e}")
    
    def fetch_article_content(self, url):
        """
        爬取文章内容
        
        参数:
            url: 文章URL
        
        返回:
            文章内容字符串
        """
        try:
            self.driver.get(url)
            time.sleep(2)
            
            # 尝试多种常见的文章内容选择器
            content_selectors = [
                'div.article-content',
                'div.content',
                'div.news-content',
                'div.detail-content',
                'article',
                'div#content',
                'div.main-content'
            ]
            
            for selector in content_selectors:
                try:
                    content_elem = self.driver.find_element(By.CSS_SELECTOR, selector)
                    content = content_elem.text.strip()
                    if content and len(content) > 100:  # 确保内容足够长
                        return content
                except:
                    continue
            
            return ""
        except Exception as e:
            print(f"    ⚠️ 内容爬取失败: {e}")
            return ""
    
    def crawl_all_sources(self, fetch_content=False):
        """
        批量爬取所有配置的新闻源
        
        参数:
            fetch_content: 是否爬取文章内容
        """
        print(f"\n{'='*60}")
        print(f"开始爬取 {self.config['sectors'][self.sector]['name']} 板块")
        print(f"{'='*60}")
        
        # 根据板块选择爬取方法
        if self.sector == 'education':
            self.crawl_mohrss()
        elif self.sector == 'healthcare':
            self.crawl_cs_com_cn()
            self.crawl_cls_cn()
            self.crawl_guandian_cn()
            self.crawl_jjckb()
        
        # 如果需要爬取文章内容
        if fetch_content and self.results:
            print(f"\n📄 开始爬取文章内容...")
            for i, news in enumerate(self.results, 1):
                print(f"  {i}/{len(self.results)}: {news['title'][:30]}...")
                content = self.fetch_article_content(news['url'])
                news['content'] = content
                time.sleep(1)  # 避免请求过快
    
    def save_results(self):
        """保存结果"""
        if not self.results:
            print("\n⚠️  没有找到任何新闻")
            return
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(script_dir, '../data/raw')
        os.makedirs(data_dir, exist_ok=True)
        
        date_str = datetime.now().strftime('%Y%m%d')
        filename = os.path.join(data_dir, f"{self.sector}_advanced_{date_str}.json")
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 已保存到: {filename}")
        print(f"📊 共保存: {len(self.results)} 条新闻")
    
    def close(self):
        """关闭浏览器"""
        self.driver.quit()


def main():
    import argparse
    parser = argparse.ArgumentParser(description='高级新闻爬虫（支持JS渲染）')
    parser.add_argument('--sector', required=True, 
                       choices=['education', 'healthcare'],
                       help='板块')
    parser.add_argument('--content', action='store_true',
                       help='是否爬取文章内容')
    args = parser.parse_args()
    
    crawler = AdvancedNewsCrawler(args.sector)
    
    try:
        crawler.crawl_all_sources(fetch_content=args.content)
        crawler.save_results()
    finally:
        crawler.close()


if __name__ == '__main__':
    main()

