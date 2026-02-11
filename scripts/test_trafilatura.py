#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Trafilatura 测试脚本
"""

import trafilatura
import time

# 测试URL列表
test_urls = [
    "https://news.google.com/rss/articles/CBMiRkFVX3lxTE1aVVZsbzJyNktVMVo1WGxVbmEwTEJ2MEVxTWlFbG9XYWNJQUJMN0F3QVBxQWs5bXpYX1VkS1gwdldHQld4dGc?oc=5&hl=en-US&gl=US&ceid=US:en",
    "http://www.xinhuanet.com/fortune/",
    "http://finance.people.com.cn/",
]

def test_trafilatura(url):
    """测试Trafilatura提取效果"""
    print(f"\n{'='*60}")
    print(f"测试URL: {url[:80]}...")
    print('='*60)
    
    try:
        start_time = time.time()
        
        # 下载网页
        downloaded = trafilatura.fetch_url(url)
        if not downloaded:
            print("❌ 下载失败")
            return None
        
        # 提取内容
        content = trafilatura.extract(
            downloaded,
            output_format='markdown',
            include_comments=False,
            include_tables=True
        )
        
        # 提取元数据
        metadata = trafilatura.extract_metadata(downloaded)
        
        elapsed = time.time() - start_time
        
        if content:
            print(f"✅ 提取成功")
            print(f"⏱️  耗时: {elapsed:.2f}秒")
            print(f"📝 内容长度: {len(content)}字符")
            
            if metadata:
                print(f"📰 标题: {metadata.title}")
                print(f"📅 日期: {metadata.date}")
                print(f"✍️  作者: {metadata.author}")
            
            print(f"\n内容预览（前500字符）:")
            print("-" * 60)
            print(content[:500])
            print("-" * 60)
            
            return content
        else:
            print(f"❌ 提取失败（耗时{elapsed:.2f}秒）")
            return None
            
    except Exception as e:
        print(f"❌ 错误: {e}")
        return None

if __name__ == '__main__':
    print("开始测试Trafilatura...")
    
    for url in test_urls:
        result = test_trafilatura(url)
        time.sleep(1)  # 避免请求过快
    
    print("\n" + "="*60)
    print("测试完成")
