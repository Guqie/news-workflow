#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高级新闻爬虫 V2 - 使用requests-html支持JavaScript渲染
"""

import json
import os
from datetime import datetime
from requests_html import HTMLSession
import time

class AdvancedNewsCrawlerV2:
    """高级新闻爬虫 - 使用requests-html"""
    
    def __init__(self, sector):
        self.sector = sector
        self.results = []
        self.config = self.load_config()
        self.keywords = self.config['sectors'][sector]['keywords']
        self.session = HTMLSession()
    
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
            r = self.session.get(url, timeout=15)
            r.html.render(timeout=20)
            
            links = r.html.find('ul.list_16 li a')
            
            count = 0
            for link in links[:30]:
                try:
                    title = link.text.strip()
                    href = link.absolute_links
                    
                    if title and len(title) > 10 and self.match_keywords(title):
                        href_url = list(href)[0] if href else url
                        self.results.append({
                            'title': title,
                            'url': href_url,
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
            r = self.session.get(url, timeout=15)
            r.html.render(timeout=20)
            
            links = r.html.find('div.news-list li a, ul.news-list li a, div.list a')
            
            count = 0
            for link in links[:30]:
                try:
                    title = link.text.strip()
                    href = link.absolute_links
                    
                    if title and len(title) > 10 and self.match_keywords(title):
                        href_url = list(href)[0] if href else url
                        self.results.append({
                            'title': title,
                            'url': href_url,
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
            r = self.session.get(url, timeout=15)
            r.html.render(timeout=20)
            
            links = r.html.find('div.depth-item a.item-title, div.article-item a')
            
            count = 0
            for link in links[:30]:
                try:
                    title = link.text.strip()
                    href = link.absolute_links
                    
                    if title and len(title) > 10 and self.match_keywords(title):
                        href_url = list(href)[0] if href else url
                        self.results.append({
                            'title': title,
                            'url': href_url,
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
            r = self.session.get(url, timeout=15)
            r.html.render(timeout=20)
            
            links = r.html.find('div.news-item a, li.news-item a, div.article a')
            
            count = 0
            for link in links[:30]:
                try:
                    title = link.text.strip()
                    href = link.absolute_links
                    
                    if title and len(title) > 10 and self.match_keywords(title):
                        href_url = list(href)[0] if href else url
                        self.results.append({
                            'title': title,
                            'url': href_url,
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
            r = self.session.get(url, timeout=15)
            links = r.html.find('ul.news-list li a, div.news-list a, div.list a')
            
            count = 0
            for link in links[:30]:
                try:
                    title = link.text.strip()
                    href = link.absolute_links
                    
                    if title and len(title) > 10 and self.match_keywords(title):
                        href_url = list(href)[0] if href else url
                        self.results.append({
                            'title': title,
                            'url': href_url,
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
            r = self.session.get(url, timeout=15)
            content_selectors = [
                'div.article-content', 'div.content', 'div.news-content',
                'div.detail-content', 'article', 'div#content'
            ]
            
            for selector in content_selectors:
                elements = r.html.find(selector)
                if elements:
                    content = elements[0].text.strip()
                    if content and len(content) > 100:
                        return content
            return ""
        except:
            return ""
    
    def crawl_all_sources(self, fetch_content=False):
        """批量爬取所有配置的新闻源"""
        print(f"\n{'='*60}")
        print(f"开始爬取 {self.config['sectors'][self.sector]['name']} 板块")
        print(f"{'='*60}")
        
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
    parser = argparse.ArgumentParser(description='高级新闻爬虫（支持JS渲染）')
    parser.add_argument('--sector', required=True, 
                       choices=['education', 'healthcare'],
                       help='板块')
    parser.add_argument('--content', action='store_true',
                       help='是否爬取文章内容')
    args = parser.parse_args()
    
    crawler = AdvancedNewsCrawlerV2(args.sector)
    crawler.crawl_all_sources(fetch_content=args.content)
    crawler.save_results()


if __name__ == '__main__':
    main()
