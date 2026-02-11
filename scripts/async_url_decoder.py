#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google News URL异步解码器
"""

from googlenewsdecoder import new_decoderv1
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def decode_single_url(url):
    """解码单个Google News URL"""
    try:
        result = new_decoderv1(url)
        if result and result.get('status'):
            return {
                'original_url': url,
                'actual_url': result['decoded_url'],
                'success': True
            }
    except Exception as e:
        pass
    
    return {
        'original_url': url,
        'actual_url': None,
        'success': False
    }

def decode_urls_async(urls, max_workers=10):
    """异步解码多个URL"""
    results = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 提交所有任务
        future_to_url = {
            executor.submit(decode_single_url, url): url 
            for url in urls
        }
        
        # 收集结果
        for future in as_completed(future_to_url):
            result = future.result()
            results.append(result)
    
    return results

# 使用示例
if __name__ == '__main__':
    # 测试URL列表
    test_urls = [
        "https://news.google.com/rss/articles/...",
        # 更多URL...
    ]
    
    start = time.time()
    results = decode_urls_async(test_urls, max_workers=10)
    elapsed = time.time() - start
    
    success_count = sum(1 for r in results if r['success'])
    print(f"处理完成：{success_count}/{len(test_urls)} 成功")
    print(f"总耗时：{elapsed:.2f}秒")
