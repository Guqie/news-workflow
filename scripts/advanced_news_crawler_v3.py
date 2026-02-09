#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高级新闻爬虫 V3 - 使用playwright支持JavaScript渲染
"""

import json
import os
from datetime import datetime
from playwright.sync_api import sync_playwright
import time

class AdvancedNewsCrawlerV3:
    """高级新闻爬虫 - 使用playwright"""
    
    def __init__(self, sector):
        self.sector = sector
        self.results = []
        self.config = self.load_config()
        self.keywords = self.config['sectors'][sector]['keywords']
        self.playwright = None
        self.browser = None
        self.page = None
    
    def load_config(self):
        """加载配置文件"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(script_dir, '../references/config.json')
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def start_browser(self):
        """启动浏览器"""
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=True)
        self.page = self.browser.new_page()
    
    def close_browser(self):
        """关闭浏览器"""
        if self.page:
            self.page.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
    
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
            self.page.goto(url, timeout=30000)
            self.page.wait_for_timeout(3000)
            
            links = self.page.query_selector_all('ul.list_16 li a')
            
            count = 0
            for link in links[:30]:
                try:
                    title = link.inner_text().strip()
                    href = link.get_attribute('href')
                    
                    if title and len(title) > 10 and self.match_keywords(title):
                        if href and not href.startswith('http'):
                            href = 'https://www.mohrss.gov.cn' + href
                        
                        self.results.append({
                            'title': title,
                            'url': href,
                            'source': '人社部',
                            'date': datetime.now().strftime('%Y-%m-%d')
                        })
                        count += 1
                except:
                    continue
            
            print(f"  ✓ 找到 {count} 条匹配新闻")
        except Exception as e:
            print(f"  ✗ 爬取失败: {e}")
    
    def crawl_cs_com_cn(self):
        """爬取中国证券报财经要闻"""
        url = "https://www.cs.com.cn/xwzx/hg/"
        print(f"\n🔍 爬取: 中国证券报财经要闻")
        
        try:
            self.page.goto(url, timeout=30000)
            self.page.wait_for_timeout(3000)
            
            # 修改选择器：直接选择带title属性的a标签
            links = self.page.query_selector_all('li a[title]')
            
            count = 0
            for link in links[:30]:
                try:
                    title = link.get_attribute('title') or link.inner_text().strip()
                    href = link.get_attribute('href')
                    
                    if title and len(title) > 10 and self.match_keywords(title):
                        if href and not href.startswith('http'):
                            href = 'https://www.cs.com.cn' + href
                        
                        self.results.append({
                            'title': title,
                            'url': href,
                            'source': '中国证券报',
                            'date': datetime.now().strftime('%Y-%m-%d')
                        })
                        count += 1
                except:
                    continue
            
            print(f"  ✓ 找到 {count} 条匹配新闻")
        except Exception as e:
            print(f"  ✗ 爬取失败: {e}")
    
    def crawl_cls_cn(self):
        """爬取财联社头条"""
        url = "https://www.cls.cn/depth?id=1000"
        print(f"\n🔍 爬取: 财联社头条")
        
        try:
            self.page.goto(url, timeout=30000)
            self.page.wait_for_timeout(3000)
            
            links = self.page.query_selector_all('div.depth-item a.item-title, div.article-item a')
            
            count = 0
            for link in links[:30]:
                try:
                    title = link.inner_text().strip()
                    href = link.get_attribute('href')
                    
                    if title and len(title) > 10 and self.match_keywords(title):
                        if href and not href.startswith('http'):
                            href = 'https://www.cls.cn' + href
                        
                        self.results.append({
                            'title': title,
                            'url': href,
                            'source': '财联社',
                            'date': datetime.now().strftime('%Y-%m-%d')
                        })
                        count += 1
                except:
                    continue
            
            print(f"  ✓ 找到 {count} 条匹配新闻")
        except Exception as e:
            print(f"  ✗ 爬取失败: {e}")
    
    def crawl_guandian_cn(self):
        """爬取观点网资讯"""
        url = "https://www.guandian.cn/news/"
        print(f"\n🔍 爬取: 观点网资讯")
        
        try:
            self.page.goto(url, timeout=30000)
            self.page.wait_for_timeout(3000)
            
            links = self.page.query_selector_all('div.news-item a, li.news-item a, div.article a')
            
            count = 0
            for link in links[:30]:
                try:
                    title = link.inner_text().strip()
                    href = link.get_attribute('href')
                    
                    if title and len(title) > 10 and self.match_keywords(title):
                        if href and not href.startswith('http'):
                            href = 'https://www.guandian.cn' + href
                        
                        self.results.append({
                            'title': title,
                            'url': href,
                            'source': '观点网',
                            'date': datetime.now().strftime('%Y-%m-%d')
                        })
                        count += 1
                except:
                    continue
            
            print(f"  ✓ 找到 {count} 条匹配新闻")
        except Exception as e:
            print(f"  ✗ 爬取失败: {e}")
    
    def crawl_jjckb(self):
        """爬取经济参考报要闻"""
        url = "http://jjckb.xinhuanet.com/yw.htm"
        print(f"\n🔍 爬取: 经济参考报要闻")
        
        try:
            self.page.goto(url, timeout=30000)
            self.page.wait_for_timeout(2000)
            
            links = self.page.query_selector_all('ul.news-list li a, div.news-list a, div.list a')
            
            count = 0
            for link in links[:30]:
                try:
                    title = link.inner_text().strip()
                    href = link.get_attribute('href')
                    
                    if title and len(title) > 10 and self.match_keywords(title):
                        self.results.append({
                            'title': title,
                            'url': href,
                            'source': '经济参考报',
                            'date': datetime.now().strftime('%Y-%m-%d')
                        })
                        count += 1
                except:
                    continue
            
            print(f"  ✓ 找到 {count} 条匹配新闻")
        except Exception as e:
            print(f"  ✗ 爬取失败: {e}")
    
    def fetch_article_content(self, url):
        """爬取文章内容"""
        try:
            self.page.goto(url, timeout=30000)
            self.page.wait_for_timeout(2000)
            
            content_selectors = [
                'div.article-content', 'div.content', 'div.news-content',
                'div.detail-content', 'article', 'div#content'
            ]
            
            for selector in content_selectors:
                try:
                    element = self.page.query_selector(selector)
                    if element:
                        content = element.inner_text().strip()
                        if content and len(content) > 100:
                            return content
                except:
                    continue
            
            return ""
        except:
            return ""
    
    def crawl_all_sources(self, fetch_content=False):
        """批量爬取所有配置的新闻源"""
        print(f"\n{'='*60}")
        print(f"开始爬取 {self.config['sectors'][self.sector]['name']} 板块")
        print(f"{'='*60}")
        
        self.start_browser()
        
        try:
            if self.sector == 'education':
                self.crawl_mohrss()
            elif self.sector == 'healthcare':
                self.crawl_cs_com_cn()
                self.crawl_cls_cn()
                self.crawl_guandian_cn()
                self.crawl_jjckb()
            
            if fetch_content and self.results:
                print(f"\n📄 开始爬取文章内容...")
                for i, news in enumerate(self.results, 1):
                    print(f"  {i}/{len(self.results)}: {news['title'][:30]}...")
                    content = self.fetch_article_content(news['url'])
                    news['content'] = content
                    time.sleep(1)
        finally:
            self.close_browser()
    
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


def main():
    import argparse
    parser = argparse.ArgumentParser(description='高级新闻爬虫V3（playwright）')
    parser.add_argument('--sector', required=True, 
                       choices=['education', 'healthcare'],
                       help='板块')
    parser.add_argument('--content', action='store_true',
                       help='是否爬取文章内容')
    args = parser.parse_args()
    
    crawler = AdvancedNewsCrawlerV3(args.sector)
    crawler.crawl_all_sources(fetch_content=args.content)
    crawler.save_results()


if __name__ == '__main__':
    main()
