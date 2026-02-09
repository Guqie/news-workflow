#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整新闻源爬虫 - 针对7个网站的专门爬取逻辑
"""

import json
import os
from datetime import datetime
from playwright.sync_api import sync_playwright
import time

class CompleteCrawler:
    """完整新闻源爬虫"""
    
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
    
    def crawl_workercn(self):
        """爬取中工网滚动新闻"""
        url = "https://www.workercn.cn/roll/"
        print(f"\n🔍 爬取: 中工网滚动新闻")
        
        try:
            self.page.goto(url, timeout=30000)
            self.page.wait_for_timeout(3000)
            
            # 中工网的新闻链接在 a 标签中，标题在 title 属性
            links = self.page.query_selector_all('a[title]')
            
            count = 0
            for link in links[:50]:
                try:
                    title = link.get_attribute('title')
                    href = link.get_attribute('href')
                    
                    if title and len(title) > 10 and self.match_keywords(title):
                        if href and not href.startswith('http'):
                            href = 'https://www.workercn.cn' + href
                        
                        self.results.append({
                            'title': title,
                            'url': href,
                            'source': '中工网',
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
            
            # 中国证券报的新闻链接在 li a[title] 中
            links = self.page.query_selector_all('li a[title]')
            
            count = 0
            for link in links[:50]:
                try:
                    title = link.get_attribute('title')
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
            
            links = self.page.query_selector_all('a')
            
            count = 0
            for link in links[:50]:
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
    
    def crawl_bjd_com_cn(self):
        """爬取京报网热点"""
        url = "https://www.bjd.com.cn/app/rdjh/redian/"
        print(f"\n🔍 爬取: 京报网热点")
        
        try:
            self.page.goto(url, timeout=30000)
            self.page.wait_for_timeout(3000)
            
            links = self.page.query_selector_all('a')
            
            count = 0
            for link in links[:50]:
                try:
                    title = link.inner_text().strip()
                    href = link.get_attribute('href')
                    
                    if title and len(title) > 10 and self.match_keywords(title):
                        if href and not href.startswith('http'):
                            href = 'https://www.bjd.com.cn' + href
                        
                        self.results.append({
                            'title': title,
                            'url': href,
                            'source': '京报网',
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
            
            links = self.page.query_selector_all('a')
            
            count = 0
            for link in links[:50]:
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
            
            links = self.page.query_selector_all('a')
            
            count = 0
            for link in links[:50]:
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
    
    def crawl_mohrss(self):
        """爬取人社部地方动态"""
        url = "https://www.mohrss.gov.cn/SYrlzyhshbzb/dongtaixinwen/dfdt/"
        print(f"\n🔍 爬取: 人社部地方动态")
        
        try:
            self.page.goto(url, timeout=30000)
            self.page.wait_for_timeout(3000)
            
            links = self.page.query_selector_all('a')
            
            count = 0
            for link in links[:50]:
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
    
    def fetch_article_content(self, url):
        """爬取文章内容"""
        try:
            self.page.goto(url, timeout=30000)
            self.page.wait_for_timeout(2000)
            
            # 尝试多种常见的文章内容选择器
            content_selectors = [
                'div.article-content',
                'div.content',
                'div.news-content',
                'div.detail-content',
                'article',
                'div#content',
                'div.main-content',
                'div.text',
                'div.article-body'
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
        """批量爬取所有新闻源"""
        print(f"\n{'='*60}")
        print(f"开始爬取所有新闻源")
        print(f"{'='*60}")
        
        self.start_browser()
        
        try:
            # 爬取所有7个网站
            self.crawl_workercn()
            self.crawl_cs_com_cn()
            self.crawl_cls_cn()
            self.crawl_bjd_com_cn()
            self.crawl_guandian_cn()
            self.crawl_jjckb()
            self.crawl_mohrss()
            
            # 如果需要爬取文章内容
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
        filename = os.path.join(data_dir, f"{self.sector}_complete_{date_str}.json")
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 已保存到: {filename}")
        print(f"📊 共保存: {len(self.results)} 条新闻")
        
        # 打印前5条新闻标题
        print(f"\n📰 前5条新闻：")
        for i, news in enumerate(self.results[:5], 1):
            print(f"{i}. {news['title']}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description='完整新闻源爬虫')
    parser.add_argument('--sector', required=True, 
                       choices=['education', 'healthcare'],
                       help='板块')
    parser.add_argument('--content', action='store_true',
                       help='是否爬取文章内容')
    args = parser.parse_args()
    
    crawler = CompleteCrawler(args.sector)
    crawler.crawl_all_sources(fetch_content=args.content)
    crawler.save_results()


if __name__ == '__main__':
    main()
