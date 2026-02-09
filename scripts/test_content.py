#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试文章内容爬取功能
"""

from playwright.sync_api import sync_playwright
import json

def test_article_content(url, title):
    """测试单个文章的内容爬取"""
    print(f"测试URL: {url}")
    print(f"标题: {title}\n")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            page.goto(url, timeout=30000)
            page.wait_for_timeout(3000)
            
            # 尝试多种选择器
            selectors = [
                'div.article-content',
                'div.content',
                'div.detail-content',
                'article',
                'div.article-body',
                'div.text'
            ]
            
            print("测试不同的选择器:\n")
            for selector in selectors:
                try:
                    element = page.query_selector(selector)
                    if element:
                        content = element.inner_text().strip()
                        print(f"✓ 选择器 '{selector}' 成功")
                        print(f"  内容长度: {len(content)} 字符")
                        print(f"  前100字: {content[:100]}...\n")
                        
                        if len(content) > 100:
                            return content
                except:
                    print(f"✗ 选择器 '{selector}' 失败\n")
            
            print("⚠️ 所有选择器都未找到内容")
            
        except Exception as e:
            print(f"✗ 爬取失败: {e}")
        finally:
            browser.close()

if __name__ == '__main__':
    # 测试财联社文章
    url = "https://www.cls.cn/detail/2282797"
    title = "工信部：开展国家算力互联互通节点建设工作 提升整体算力水平"
    test_article_content(url, title)
