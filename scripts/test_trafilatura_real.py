#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Trafilatura 实际新闻文章测试
"""

import trafilatura
import time

# 实际的新闻文章URL（手动选择）
test_urls = [
    # 新华网科技新闻
    "http://www.news.cn/tech/20250211/c_1212345678.htm",
    # 人民网财经新闻  
    "http://finance.people.com.cn/n1/2025/0211/c1004-12345678.html",
    # 科技日报
    "https://www.stdaily.com/index/kejixinwen/202502/11/content_12345.shtml",
]

def test_single_url(url):
    """测试单个URL"""
    print(f"\n{'='*70}")
    print(f"测试URL: {url}")
    print('='*70)
    
    try:
        start_time = time.time()
        downloaded = trafilatura.fetch_url(url)
        
        if not downloaded:
            print("❌ 下载失败")
            return False
        
        content = trafilatura.extract(
            downloaded,
            output_format='markdown',
            include_comments=False,
            include_tables=True
        )
        
        metadata = trafilatura.extract_metadata(downloaded)
        elapsed = time.time() - start_time
        
        if content and len(content) > 100:
            print(f"✅ 提取成功")
            print(f"⏱️  耗时: {elapsed:.2f}秒")
            print(f"📝 内容长度: {len(content)}字符")
            
            if metadata:
                if metadata.title:
                    print(f"📰 标题: {metadata.title}")
                if metadata.date:
                    print(f"📅 日期: {metadata.date}")
            
            print(f"\n内容预览（前300字符）:")
            print("-" * 70)
            print(content[:300])
            print("-" * 70)
            return True
        else:
            print(f"❌ 提取失败或内容过短（{len(content) if content else 0}字符）")
            return False
            
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False

if __name__ == '__main__':
    print("Trafilatura 实际新闻测试")
    print("注意：这些URL可能不存在，仅用于测试流程")
    
    success_count = 0
    for url in test_urls:
        if test_single_url(url):
            success_count += 1
        time.sleep(1)
    
    print(f"\n{'='*70}")
    print(f"测试完成：成功 {success_count}/{len(test_urls)}")
