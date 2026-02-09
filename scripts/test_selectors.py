#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本 - 不使用关键词过滤，查看能提取多少新闻
"""

from playwright.sync_api import sync_playwright

url = "https://www.cs.com.cn/xwzx/hg/"
print(f"测试网站: {url}\n")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    page.goto(url, timeout=30000)
    page.wait_for_timeout(3000)
    
    # 测试不同的选择器
    selectors = [
        'li a[title]',
        'li a',
        'a[title]',
        'div a',
    ]
    
    for selector in selectors:
        links = page.query_selector_all(selector)
        print(f"选择器 '{selector}': 找到 {len(links)} 个链接")
        
        if links and len(links) > 0:
            print("  前5个链接:")
            for i, link in enumerate(links[:5], 1):
                title = link.get_attribute('title') or link.inner_text().strip()
                href = link.get_attribute('href')
                print(f"    {i}. {title[:50]}... | {href[:50]}...")
            print()
    
    browser.close()
