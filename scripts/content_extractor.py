#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新闻内容提取器 - 集成URL解码和内容提取
"""

from googlenewsdecoder import new_decoderv1
from concurrent.futures import ThreadPoolExecutor, as_completed
import trafilatura
import time

class NewsContentExtractor:
    """新闻内容提取器"""
    
    def __init__(self, max_workers=10):
        self.max_workers = max_workers
    
    def decode_google_news_url(self, url):
        """解码Google News URL"""
        try:
            if 'news.google.com' in url:
                result = new_decoderv1(url)
                if result and result.get('status'):
                    return result['decoded_url']
        except:
            pass
        return url
    
    def extract_content(self, url):
        """提取新闻内容"""
        try:
            downloaded = trafilatura.fetch_url(url)
            if downloaded:
                content = trafilatura.extract(
                    downloaded,
                    output_format='markdown',
                    include_comments=False,
                    include_tables=True
                )
                return content
        except:
            pass
        return None
    
    def process_single_news(self, news_item):
        """处理单条新闻：解码URL + 提取内容"""
        try:
            # 1. 解码URL
            actual_url = self.decode_google_news_url(news_item['url'])
            
            # 2. 提取内容
            content = self.extract_content(actual_url)
            
            # 3. 更新新闻项
            news_item['actual_url'] = actual_url
            news_item['content'] = content if content else ''
            news_item['has_content'] = bool(content)
            
            return news_item
        except Exception as e:
            news_item['actual_url'] = news_item['url']
            news_item['content'] = ''
            news_item['has_content'] = False
            return news_item
    
    def process_news_list_async(self, news_list):
        """异步处理新闻列表"""
        print(f"\n开始异步处理 {len(news_list)} 条新闻...")
        start_time = time.time()
        
        results = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_news = {
                executor.submit(self.process_single_news, news): news
                for news in news_list
            }
            
            completed = 0
            for future in as_completed(future_to_news):
                result = future.result()
                results.append(result)
                completed += 1
                
                # 每处理100条显示进度
                if completed % 100 == 0:
                    print(f"  进度: {completed}/{len(news_list)}")
        
        elapsed = time.time() - start_time
        success_count = sum(1 for r in results if r['has_content'])
        
        print(f"✅ 处理完成")
        print(f"⏱️  总耗时: {elapsed:.1f}秒")
        print(f"📝 成功提取内容: {success_count}/{len(news_list)}")
        
        return results
